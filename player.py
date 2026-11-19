"""Reproductor DJ/VJ embebido (HTML/JS). Se actualiza solo por MQTT, sin recargar Streamlit."""
from pathlib import Path

import streamlit.components.v1 as components

from config import BASE, BPM_BASE

_TEMPLATE = (Path(__file__).parent / "player.html").read_text(encoding="utf-8")


def render_player(voice: bool = False, height: int = 480):
    html = (_TEMPLATE.replace("__BASE__", BASE)
                     .replace("__VOICE__", "true" if voice else "false")
                     .replace("__BPM_BASE__", str(BPM_BASE)))
    components.html(html, height=height)
