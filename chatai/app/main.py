"""
Private character chat — FastAPI app entrypoint.

Fully local by default: binds to 127.0.0.1, stores everything as plain
JSON files under ./data, and only ever talks to the model server you
configure in Settings (Ollama on localhost by default). No analytics,
no accounts, no cloud dependency of any kind.

The frontend is also an installable PWA, so it can be added to an iPhone
home screen and run full-screen against the server on your own machine —
see the README for the LAN/HTTPS setup that needs.
"""
from __future__ import annotations

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

from . import auth, config
from .routers import characters, chats, generate, personas, settings as settings_router

app = FastAPI(title="Private Character Chat", docs_url="/api/docs")

# No-op unless CHATAI_PASSCODE is set (see app/auth.py).
app.add_middleware(auth.PasscodeMiddleware)

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


# ---------- PWA plumbing ----------
#
# These three have to live at the site root: the service worker can only
# control pages at or below its own path, and the manifest/offline page
# are fetched relative to it.


@app.get("/sw.js")
def service_worker():
    return FileResponse(
        config.WEB_DIR / "sw.js",
        media_type="application/javascript",
        headers={
            # Always revalidate the worker itself, so a change to the app
            # ships on the next launch instead of sticking for a day.
            "Cache-Control": "no-cache",
            "Service-Worker-Allowed": "/",
        },
    )


@app.get("/manifest.webmanifest")
def manifest():
    return FileResponse(
        config.WEB_DIR / "manifest.webmanifest",
        media_type="application/manifest+json",
        headers={"Cache-Control": "no-cache"},
    )


@app.get("/offline.html")
def offline():
    return FileResponse(config.WEB_DIR / "offline.html")


@app.get("/favicon.ico")
def favicon():
    return FileResponse(config.WEB_DIR / "static" / "icons" / "favicon-32.png",
                        media_type="image/png")


# Safari looks for this at the root if a page ever loads without our
# <link rel="apple-touch-icon">.
@app.get("/apple-touch-icon.png")
@app.get("/apple-touch-icon-precomposed.png")
def apple_touch_icon():
    return FileResponse(config.WEB_DIR / "static" / "icons" / "apple-touch-icon-180.png",
                        media_type="image/png")


# ---------- Optional passcode gate ----------


@app.get("/login")
def login_form(request: Request):
    if not config.PASSCODE or auth.is_authorized(request):
        return Response(status_code=303, headers={"Location": "/"})
    return auth.login_page()


@app.post("/login")
def login_submit(request: Request, passcode: str = Form("")):
    if not config.PASSCODE:
        return Response(status_code=303, headers={"Location": "/"})
    return auth.do_login(request, passcode)


@app.get("/health")
def health():
    return {"status": "ok"}
