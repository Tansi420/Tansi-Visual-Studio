# Tansi Visual Studio · controlador DJ/VJ multimodal (Wokwi + Streamlit + MQTT)

Dos ambientes que controlan la misma mezcla de 4 audios (140 BPM) y 4 visuales en loop:

| Ambiente | Página | Modalidades |
|---|---|---|
| Físico | **Escenario físico** | 8 pads, 2 potenciómetros (volumen, BPM) y LEDs en un ESP32 simulado en Wokwi |
| Digital | **Control digital** | voz, texto, selectores, sliders y botones |

## Arquitectura
```
Wokwi (ESP32) ──cmd/*──►  Backend (Streamlit + paho) ──estado/* (retained)──► Wokwi (LEDs, LED beat)
Voz (navegador) ─cmd/texto─►        │                                    └──► Reproductor HTML/JS (WSS)
Controles web ───────────────►      └ estado único + intérprete de comandos
```
Tópicos bajo `BASE`: `cmd/{audio,video,volumen,bpm,texto,invierte,silencio}` y `estado/{audio,video,volumen,bpm,invierte,silencio}`.

## Ejecutar
1. Elige un `BASE` único y úsalo igual en `config.py` (o variable `IMM_BASE`) y en `wokwi/sketch.ino`.
2. `pip install -r requirements.txt`
3. `streamlit run app.py` (desde esta carpeta) y abre la app en **Chrome o Edge**.
4. En wokwi.com crea un proyecto ESP32, pega `wokwi/sketch.ino`, `diagram.json` y `libraries.txt` y dale play.
5. En el reproductor haz clic en **INICIAR SHOW** (el navegador exige un clic para activar el audio). Hay que repetirlo al cambiar de página.

## Comandos de voz / texto
`invierte` · `silencio` (alterna) · `más rápido` / `más lento` (±10 BPM; el tono cambia como un vinilo).

## Notas
- Videos transcodificados de HEVC `.mov` a H.264 `.mp4` (sin pista de audio) para que reproduzcan en cualquier navegador.
- Velocidad de reproducción = BPM / 140. Rango 100–180 BPM.

## Diseño (estética web 2000)
- `ui.py`: tema global (CSS), cabecera, paneles, lecturas y terminal. Fuentes de Google Fonts: Pixelify Sans, Silkscreen y VT323 (necesitan internet).
- `static/ui/`: GIFs pixelados generados con `python tools/make_assets.py` (puedes reemplazarlos por los tuyos con el mismo nombre).
- Los widgets de la mesa de mezcla tienen claves fijas y se sincronizan con el estado real antes de dibujarse (evita elementos duplicados).
- Fondo: `static/ui/bg.jpg` (foto optimizada, con velo violeta en `ui.py`). Para cambiarlo, reemplaza el archivo.
- GIFs decorativos: `static/ui/deco/*.gif`. Su reparto (riel derecho, barra lateral, cabecera, franjas) está en las listas `RAIL`, `SIDE`, `HEAD`, `STRIP_B` y `STRIP_C` de `ui.py`.
- Iconos de los pads: `botonmusica.gif` (audio) y `botonvideo.gif` (visual), aplicados por CSS a los botones `pad_audio_*` y `pad_video_*`.
