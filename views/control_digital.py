"""Ambiente 2 – Digital: voz, texto y mesa de mezcla web (misma mezcla, otras modalidades)."""
import hashlib

import streamlit as st

import ui
from backend import get_backend
from config import BPM_BASE, BPM_MAX, BPM_MIN
from player import render_player

try:
    import speech_recognition as sr
except ImportError:          # pip install SpeechRecognition
    sr = None

be = get_backend()


def transcribir(audio_file) -> str:
    """WAV grabado por st.audio_input -> texto (servicio web gratuito de Google)."""
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as fuente:
        return r.recognize_google(r.record(fuente), language="es-CO")


# ---- callbacks: aplican el cambio en el backend (que lo publica por MQTT) ----
def _pad(nombre: str, n: int):
    be.apply(nombre, n, "web")


def _slider(nombre: str):
    be.apply(nombre, st.session_state[f"w_{nombre}"], "web")


def _toggle(nombre: str):
    be.apply(nombre, 1 - be.snapshot()[nombre], "web")


ui.header("AMBIENTE 2 · CONTROL DIGITAL")
st.caption("Habla (botón 🎤 del reproductor o la grabadora), escribe o usa la mesa de mezcla. "
           "Todo se refleja en los LEDs de Wokwi.")

render_player(voice=True, height=480)
ui.chevrons()
ui.strip(ui.STRIP_B)

izq, der = st.columns(2)

with izq:
    with st.container(border=True):
        ui.ptitle("Comandos de texto")
        with st.form("cmd_texto", clear_on_submit=True):
            texto = st.text_input("Escribe un comando",
                                  placeholder="invierte · silencio · más rápido · más lento")
            enviado = st.form_submit_button("ENVIAR")
        if enviado and texto.strip():
            st.info(be.interpret(texto, "texto"))
        st.markdown('<div class="tips"><ul><li><b>invierte</b>: colores del visual</li>'
                    '<li><b>silencio</b>: corte on/off</li>'
                    '<li><b>más rápido / más lento</b>: ±10 BPM (efecto vinilo)</li></ul></div>',
                    unsafe_allow_html=True)

    with st.container(border=True):
        ui.ptitle("Comandos de voz (grabadora)")
        if sr is None:
            st.warning("Falta la librería: `pip3 install SpeechRecognition`")
        else:
            grabacion = st.audio_input("Graba un comando y detén la grabación")
            if grabacion is not None:
                datos = grabacion.getvalue()
                huella = hashlib.md5(datos).hexdigest()
                if st.session_state.get("ultima_voz") != huella:      # cada grabación se procesa una sola vez
                    st.session_state["ultima_voz"] = huella
                    try:
                        st.info(be.interpret(transcribir(grabacion), "voz"))
                    except sr.UnknownValueError:
                        st.warning("No entendí el audio, intenta de nuevo.")
                    except Exception as e:
                        st.error(f"No se pudo transcribir: {e}")


@st.fragment(run_every=2)
def mesa_de_mezcla():
    """Todos los widgets tienen clave fija (no cambian de identidad); los sliders se
    sincronizan con el estado real antes de dibujarse, así siguen a los faders de Wokwi."""
    s = be.snapshot()
    for k in ("volumen", "bpm"):
        if st.session_state.get(f"_seen_{k}") != s[k]:
            st.session_state[f"w_{k}"] = s[k]
            st.session_state[f"_seen_{k}"] = s[k]

    for nombre, etiqueta in (("audio", "AUDIO"), ("video", "VISUAL")):
        st.markdown(f"**{etiqueta}**")
        cols = st.columns(4)
        for i in range(1, 5):
            cols[i - 1].button(f"{etiqueta} {i}", key=f"pad_{nombre}_{i}", on_click=_pad, args=(nombre, i),
                               type="primary" if s[nombre] == i else "secondary")
    st.slider("VOLUMEN", 0, 100, key="w_volumen", on_change=_slider, args=("volumen",))
    st.slider(f"BPM (original {BPM_BASE})", BPM_MIN, BPM_MAX, key="w_bpm", on_change=_slider, args=("bpm",))
    c1, c2 = st.columns(2)
    c1.button("INVIERTE", key="btn_inv", on_click=_toggle, args=("invierte",),
              type="primary" if s["invierte"] else "secondary")
    c2.button("SILENCIO", key="btn_sil", on_click=_toggle, args=("silencio",),
              type="primary" if s["silencio"] else "secondary")


with der:
    with st.container(border=True):
        ui.ptitle("Mesa de mezcla")
        mesa_de_mezcla()


@st.fragment(run_every=1)
def eventos():
    st.markdown(ui.log_html(be.log_rows(6)), unsafe_allow_html=True)


with st.container(border=True):
    ui.ptitle("Registro de eventos")
    eventos()

ui.footer()
