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

LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


def is_lan_exposed() -> bool:
    """True when the app is bound to something other than loopback."""
    return HOST not in LOOPBACK_HOSTS


# Optional shared passcode. Only relevant when you deliberately expose the
# app to your LAN (e.g. to reach it from a phone): with it set, a browser
# has to enter it once before it can see any chats. Empty = no gate, which
# is fine while the app is loopback-only.
PASSCODE = os.environ.get("CHATAI_PASSCODE", "").strip()

# Key used to sign the auth cookie. Generated once, kept out of git, and
# never leaves this machine; deleting it just logs every device out.
SECRET_FILE = DATA_DIR / ".session_secret"


def session_secret() -> bytes:
    import secrets

    if SECRET_FILE.exists():
        data = SECRET_FILE.read_bytes().strip()
        if data:
            return data
    data = secrets.token_hex(32).encode()
    SECRET_FILE.write_bytes(data)
    try:
        SECRET_FILE.chmod(0o600)
    except OSError:
        pass  # Windows / exotic filesystems
    return data
