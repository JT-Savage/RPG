"""
Private character chat — FastAPI app entrypoint.

Fully local by default: binds to 127.0.0.1, stores everything as plain
JSON files under ./data, and only ever talks to the model server you
configure in Settings (Ollama on localhost by default). No analytics,
no accounts, no cloud dependency of any kind.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from . import config
from .routers import characters, chats, generate, personas, settings as settings_router

app = FastAPI(title="Private Character Chat", docs_url="/api/docs")

app.include_router(characters.router)
app.include_router(personas.router)
app.include_router(chats.router)
app.include_router(generate.router)
app.include_router(settings_router.router)

# Serve uploaded character/persona avatars from the data directory.
app.mount("/media/characters", StaticFiles(directory=config.CHARACTERS_DIR), name="char-media")
app.mount("/media/personas", StaticFiles(directory=config.PERSONAS_DIR), name="persona-media")

# Serve the frontend's static assets, then the SPA shell for everything else.
app.mount("/static", StaticFiles(directory=config.WEB_DIR / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(config.WEB_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}
