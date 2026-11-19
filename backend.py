"""Backend MQTT: estado único del show + intérprete de comandos de voz/texto.

Flujo:  Wokwi / navegador (voz) / controles web  --cmd/*-->  Backend
        Backend  --estado/* (retained)-->  Wokwi (LEDs) y reproductor (audio/video)
"""
import threading
import time
import unicodedata
import re
from collections import deque

import paho.mqtt.client as mqtt
import streamlit as st

from config import BASE, BROKER, PORT, BPM_BASE, BPM_MIN, BPM_MAX, BPM_STEP

DEFAULTS = {"audio": 1, "video": 1, "volumen": 80, "bpm": BPM_BASE, "invierte": 0, "silencio": 0}
LIMITS = {"audio": (1, 4), "video": (1, 4), "volumen": (0, 100), "bpm": (BPM_MIN, BPM_MAX),
          "invierte": (0, 1), "silencio": (0, 1)}
SOURCES = {"wokwi": "Wokwi", "web": "Web", "voz": "Voz", "texto": "Texto"}


def _norm(text: str) -> str:
    """minúsculas y sin tildes: 'Más Rápido' -> 'mas rapido'."""
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


# Comandos de voz/texto. El orden importa: "desacelera" se evalúa antes que "acelera".
COMMANDS = [
    ("invierte", re.compile(r"invier|invert"), "toggle"),
    ("silencio", re.compile(r"silencio|mute|callate"), "toggle"),
    ("bpm", re.compile(r"mas lento|mas despacio|desacelera|frena"), -BPM_STEP),
    ("bpm", re.compile(r"mas rapido|mas veloz|(?<!des)acelera"), +BPM_STEP),
]


class Backend:
    def __init__(self):
        self.state = dict(DEFAULTS)
        self.log = deque(maxlen=60)
        self.connected = False
        self._lock = threading.Lock()
        self._client = self._make_client()
        self._client.connect_async(BROKER, PORT, keepalive=30)
        self._client.loop_start()

    # ---------- MQTT ----------
    def _make_client(self):
        cid = f"streamlit-imm-{int(time.time()) % 100000}"
        try:                                    # paho-mqtt 2.x
            c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=cid)
        except AttributeError:                  # paho-mqtt 1.x
            c = mqtt.Client(client_id=cid)
        c.on_connect = self._on_connect
        c.on_disconnect = self._on_disconnect
        c.on_message = self._on_message
        c.reconnect_delay_set(1, 5)
        return c

    def _on_connect(self, client, userdata, flags, rc, *args):
        self.connected = True
        client.subscribe(f"{BASE}/cmd/#")
        for name, value in self.snapshot().items():       # re-publica el estado (retained)
            client.publish(f"{BASE}/estado/{name}", str(value), retain=True)

    def _on_disconnect(self, *args):
        self.connected = False

    def _on_message(self, client, userdata, msg):
        name = msg.topic.rsplit("/", 1)[-1]
        payload = msg.payload.decode("utf-8", errors="ignore").strip()
        if name == "texto":
            self.interpret(payload, "voz")
        elif name in LIMITS:
            self._apply_payload(name, payload, "wokwi")

    # ---------- Estado ----------
    def snapshot(self) -> dict:
        with self._lock:
            return dict(self.state)

    def _apply_payload(self, name, payload, source):
        if payload == "toggle":
            value = 1 - self.snapshot()[name]
        else:
            try:
                value = int(float(payload))
            except ValueError:
                return
        self.apply(name, value, source)

    def apply(self, name: str, value: int, source: str = "web", log: bool = True):
        lo, hi = LIMITS[name]
        value = max(lo, min(hi, int(value)))
        with self._lock:
            changed = self.state[name] != value
            self.state[name] = value
        # Siempre se publica: así Wokwi y el reproductor se resincronizan.
        self._client.publish(f"{BASE}/estado/{name}", str(value), retain=True)
        if changed and log:
            self._log(source, f"{name} = {value}")

    def _log(self, source, text):
        now = time.time()
        if self.log and self.log[0]["_k"] == (source, text.split(" ")[0]) and now - self.log[0]["_t"] < 1.0 \
                and text.split(" ")[0] in ("volumen", "bpm"):
            self.log.popleft()                 # agrupa el barrido continuo de una perilla
        self.log.appendleft({"_t": now, "_k": (source, text.split(" ")[0]),
                             "Hora": time.strftime("%H:%M:%S"), "Origen": SOURCES.get(source, source),
                             "Evento": text})

    def log_rows(self, n=10):
        return [{k: v for k, v in r.items() if not k.startswith("_")} for r in list(self.log)[:n]]

    # ---------- Comandos de voz / texto ----------
    def interpret(self, text: str, source: str = "texto") -> str:
        """Interpreta una frase y aplica los comandos reconocidos. Devuelve un mensaje para la UI."""
        norm = _norm(text)
        done = []
        for name, pattern, action in COMMANDS:
            if not pattern.search(norm):
                continue
            current = self.snapshot()[name]
            value = 1 - current if action == "toggle" else current + action
            self.apply(name, value, source, log=False)
            done.append(f"{name} = {self.snapshot()[name]}")
        if not done:
            self._log(source, f"«{text}» (sin comando)")
            return f"No reconocí ningún comando en «{text}»."
        self._log(source, f"«{text}» → " + ", ".join(done))
        return f"«{text}» → " + ", ".join(done)


@st.cache_resource
def get_backend() -> Backend:
    """Una sola instancia (y una sola conexión MQTT) para todas las páginas y reruns."""
    return Backend()
