"""Ambiente 1 – Físico: pads, faders y LEDs del ESP32 (Wokwi) controlan el show."""
import streamlit as st

import ui
from backend import get_backend
from player import render_player

be = get_backend()

ui.header("AMBIENTE 1 · ESCENARIO FÍSICO")
st.caption("Los pads y faders del ESP32 en Wokwi mandan en esta pista; "
           "la app confirma el estado y Wokwi lo enciende en sus LEDs.")

render_player(voice=False, height=480)
ui.chevrons()
ui.strip(ui.STRIP_B)


@st.fragment(run_every=1)
def panel_estado():
    st.markdown(ui.status_html(be.connected, be.snapshot()), unsafe_allow_html=True)
    st.markdown(ui.log_html(be.log_rows(8)), unsafe_allow_html=True)


with st.container(border=True):
    ui.ptitle("Estado en vivo")
    panel_estado()

ui.footer()
