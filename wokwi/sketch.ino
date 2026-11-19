// Proyecto Final - Interfaces Multimodales (controlador DJ/VJ)
// ESP32 (Wokwi): 4 pads de audio + 4 de visual, 8 LEDs de estado,
// potenciómetro de volumen, potenciómetro de BPM y LED "beat".
//
// Wokwi -> app : BASE/cmd/audio | cmd/video   ("1".."4")
//                BASE/cmd/volumen             ("0".."100")
//                BASE/cmd/bpm                 ("100".."180")
// app -> Wokwi : BASE/estado/audio | estado/video  (retained, "1".."4")
//                BASE/estado/bpm                   (retained, "100".."180")
#include <WiFi.h>
#include <PubSubClient.h>

// !!! Cambia BASE por algo único tuyo (el broker es público y compartido) !!!
const char* BASE   = "imm2026/tunombre";
const char* BROKER = "broker.hivemq.com";
const int   PORT   = 1883;

const int BTN_AUDIO[4] = {13, 14, 27, 26};
const int BTN_VIDEO[4] = {25, 33, 32, 23};
const int LED_AUDIO[4] = {15, 2, 4, 16};
const int LED_VIDEO[4] = {17, 5, 18, 19};
const int POT_VOL = 34;   // ADC1 (solo entrada)
const int POT_BPM = 35;   // ADC1 (solo entrada)
const int LED_BEAT = 22;

WiFiClient espClient;
PubSubClient mqtt(espClient);

unsigned long lastPress[8] = {0};
bool lastState[8];
char tCmdA[64], tCmdV[64], tCmdVol[64], tCmdBpm[64];
char tEstA[64], tEstV[64], tEstBpm[64];

int bpm = 140;                       // BPM vigente (lo confirma la app)
int lastVolSent = -1, lastBpmSent = -1;
float volFilt = 0, bpmFilt = 0;
unsigned long lastPot = 0, lastBeat = 0;
bool beatOn = false;

void setLeds(const int* leds, int activo) {          // activo: 1..4
  for (int i = 0; i < 4; i++) digitalWrite(leds[i], (i + 1 == activo) ? HIGH : LOW);
}

void onMessage(char* topic, byte* payload, unsigned int len) {
  String msg;
  for (unsigned int i = 0; i < len; i++) msg += (char)payload[i];
  int n = msg.toInt();
  String t = String(topic);
  if (t == tEstA && n >= 1 && n <= 4) setLeds(LED_AUDIO, n);
  else if (t == tEstV && n >= 1 && n <= 4) setLeds(LED_VIDEO, n);
  else if (t == tEstBpm && n >= 40 && n <= 240) bpm = n;
  Serial.printf("Estado recibido %s -> %d\n", topic, n);
}

void connectWifi() {
  WiFi.begin("Wokwi-GUEST", "", 6);
  while (WiFi.status() != WL_CONNECTED) { delay(200); Serial.print("."); }
  Serial.println("\nWiFi OK");
}

void connectMqtt() {
  while (!mqtt.connected()) {
    String id = "esp32-imm-" + String(random(0xffff), HEX);
    if (mqtt.connect(id.c_str())) {
      mqtt.subscribe(tEstA);
      mqtt.subscribe(tEstV);
      mqtt.subscribe(tEstBpm);
      Serial.println("MQTT OK");
    } else delay(1000);
  }
}

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 4; i++) {
    pinMode(BTN_AUDIO[i], INPUT_PULLUP); pinMode(BTN_VIDEO[i], INPUT_PULLUP);
    pinMode(LED_AUDIO[i], OUTPUT);       pinMode(LED_VIDEO[i], OUTPUT);
  }
  pinMode(LED_BEAT, OUTPUT);
  for (int i = 0; i < 8; i++) lastState[i] = HIGH;
  snprintf(tCmdA, 64, "%s/cmd/audio", BASE);     snprintf(tCmdV, 64, "%s/cmd/video", BASE);
  snprintf(tCmdVol, 64, "%s/cmd/volumen", BASE); snprintf(tCmdBpm, 64, "%s/cmd/bpm", BASE);
  snprintf(tEstA, 64, "%s/estado/audio", BASE);  snprintf(tEstV, 64, "%s/estado/video", BASE);
  snprintf(tEstBpm, 64, "%s/estado/bpm", BASE);
  volFilt = analogRead(POT_VOL); bpmFilt = analogRead(POT_BPM);
  connectWifi();
  mqtt.setServer(BROKER, PORT);
  mqtt.setCallback(onMessage);
}

void checkButton(int idx, int pin, const char* topic, int valor) {
  bool s = digitalRead(pin);
  if (lastState[idx] == HIGH && s == LOW && millis() - lastPress[idx] > 50) {
    lastPress[idx] = millis();
    mqtt.publish(topic, String(valor).c_str());
    Serial.printf("Pad -> %s = %d\n", topic, valor);
  }
  lastState[idx] = s;
}

// Lee los potenciómetros (con filtro) y publica solo si cambian lo suficiente
void checkPots() {
  if (millis() - lastPot < 100) return;
  lastPot = millis();
  volFilt = 0.7 * volFilt + 0.3 * analogRead(POT_VOL);
  bpmFilt = 0.7 * bpmFilt + 0.3 * analogRead(POT_BPM);
  int vol = map((int)volFilt, 0, 4095, 0, 100);
  int b   = map((int)bpmFilt, 0, 4095, 100, 180);
  if (abs(vol - lastVolSent) >= 2) {
    lastVolSent = vol;
    mqtt.publish(tCmdVol, String(vol).c_str());
    Serial.printf("Volumen -> %d\n", vol);
  }
  if (abs(b - lastBpmSent) >= 2) {
    lastBpmSent = b;
    mqtt.publish(tCmdBpm, String(b).c_str());
    Serial.printf("BPM -> %d\n", b);
  }
}

// LED amarillo: parpadea al ritmo del BPM confirmado por la app
void updateBeat() {
  unsigned long period = 60000UL / bpm;
  if (millis() - lastBeat >= period) {
    lastBeat = millis();
    beatOn = true;
    digitalWrite(LED_BEAT, HIGH);
  } else if (beatOn && millis() - lastBeat > 60) {
    beatOn = false;
    digitalWrite(LED_BEAT, LOW);
  }
}

void loop() {
  if (!mqtt.connected()) connectMqtt();
  mqtt.loop();
  for (int i = 0; i < 4; i++) {
    checkButton(i,     BTN_AUDIO[i], tCmdA, i + 1);
    checkButton(4 + i, BTN_VIDEO[i], tCmdV, i + 1);
  }
  checkPots();
  updateBeat();
}
