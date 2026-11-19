"""Configuración compartida. BASE debe ser IDÉNTICA a la del sketch de Wokwi."""
import os

BASE = os.getenv("IMM_BASE", "imm2026/tansibeats")   # <-- cámbialo por algo único tuyo
BROKER = "broker.hivemq.com"                        # broker público (TCP 1883 / WSS 8884)
PORT = 1883

BPM_BASE = 140                  # BPM original de los 4 audios (velocidad 1.0x)
BPM_MIN, BPM_MAX = 100, 180     # rango del potenciómetro y de los comandos de voz
BPM_STEP = 10                   # paso de "más rápido" / "más lento"
