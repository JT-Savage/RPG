"""
Application configuration.

Everything here is local-only: file paths on disk and network settings
for the *model backend* the user chooses to run themselves (e.g. Ollama
or an OpenAI-compatible local server). This app never phones home and
never talks to any third-party service unless the user explicitly types
a remote base_url into Settings.
"""
from __future__ import annotations

import os
from pathlib import Path

# Root of the chatai package (…/chatai)
BASE_DIR = Path(__file__).resolve().parent.parent

# All runtime data (characters, personas, chats, settings) lives under
# DATA_DIR as plain JSON files. Nothing here is ever uploaded anywhere.
DATA_DIR = Path(os.environ.get("CHATAI_DATA_DIR", BASE_DIR / "data")).resolve()
CHARACTERS_DIR = DATA_DIR / "characters"
PERSONAS_DIR = DATA_DIR / "personas"
CHATS_DIR = DATA_DIR / "chats"
SETTINGS_FILE = DATA_DIR / "settings.json"

WEB_DIR = BASE_DIR / "web"

for d in (DATA_DIR, CHARACTERS_DIR, PERSONAS_DIR, CHATS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Bind address. Defaults to loopback-only so the app is reachable only
# from this machine. Set CHATAI_HOST=0.0.0.0 yourself if you deliberately
# want it reachable from other devices on your LAN (e.g. your phone).
HOST = os.environ.get("CHATAI_HOST", "127.0.0.1")
PORT = int(os.environ.get("CHATAI_PORT", "8765"))
