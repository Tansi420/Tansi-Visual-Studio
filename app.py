"""Punto de entrada: streamlit run app.py  (app multipágina con dos ambientes)."""
import streamlit as st

st.set_page_config(page_title="Tansi Visual Studio", page_icon="👁️", layout="wide")

import ui  # noqa: E402  (después de set_page_config)

ui.inject_theme()
with st.sidebar:
    ui.sidebar_decor()

pages = [
    st.Page("views/escenario.py", title="Escenario físico", icon="🎛️", default=True),
    st.Page("views/control_digital.py", title="Control digital", icon="🎤"),
]
st.navigation(pages).run()
