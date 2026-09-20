"""
Optional passcode gate.

The app is loopback-only by default, where a login screen would be pure
friction. But the whole point of the PWA is using it from a phone, which
means binding to the LAN — and then every other device on that Wi-Fi can
read your chats. Setting CHATAI_PASSCODE puts a single shared passcode in
front of everything; a browser that passes it once gets a signed cookie
and stays logged in.

This is deliberately small: one shared secret, no accounts, no user
database. It is a lock on your own LAN, not an authentication system for
the open internet — don't port-forward this.
"""
from __future__ import annotations

import hmac
import time
from hashlib import sha256

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

from . import config

COOKIE_NAME = "chatai_auth"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # a year; it's your own device

# Paths reachable without the passcode: the login screen itself and the
# static shell the browser needs to render it (plus the PWA plumbing, so
# an installed app can still boot and show the login page).
PUBLIC_PATHS = {
    "/login",
    "/health",
    "/manifest.webmanifest",
    "/sw.js",
    "/offline.html",
    "/favicon.ico",
}
PUBLIC_PREFIXES = ("/static/",)

# Crude brute-force brake: a handful of tries per address per window.
_MAX_FAILURES = 8
_WINDOW_SECONDS = 300
_failures: dict[str, list[float]] = {}


def expected_token() -> str:
    """The cookie value that proves the passcode was entered."""
    return hmac.new(config.session_secret(), config.PASSCODE.encode(), sha256).hexdigest()


def is_authorized(request: Request) -> bool:
    if not config.PASSCODE:
        return True
    cookie = request.cookies.get(COOKIE_NAME, "")
    return hmac.compare_digest(cookie, expected_token())


def _client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _throttled(key: str) -> bool:
    now = time.time()
    hits = [t for t in _failures.get(key, []) if now - t < _WINDOW_SECONDS]
    _failures[key] = hits
    return len(hits) >= _MAX_FAILURES


def _record_failure(key: str) -> None:
    _failures.setdefault(key, []).append(time.time())


class PasscodeMiddleware(BaseHTTPMiddleware):
    """Blocks everything but PUBLIC_PATHS until the passcode cookie is set."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if (not config.PASSCODE
                or path in PUBLIC_PATHS
                or path.startswith(PUBLIC_PREFIXES)
                or is_authorized(request)):
            return await call_next(request)

        if path.startswith("/api/"):
            return Response('{"detail":"Passcode required"}', status_code=401,
                            media_type="application/json")
        return RedirectResponse("/login", status_code=303)


LOGIN_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#14151a" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <link rel="manifest" href="/manifest.webmanifest" />
  <link rel="apple-touch-icon" href="/static/icons/apple-touch-icon-180.png" />
  <title>Passcode — Private Character Chat</title>
  <link rel="stylesheet" href="/static/style.css" />
</head>
<body>
  <div class="offline-shell">
    <form method="post" action="/login" class="empty-state" style="max-width:340px">
      <h2>Private Character Chat</h2>
      <p>__MESSAGE__</p>
      <div class="field">
        <input type="password" name="passcode" autocomplete="current-password"
               inputmode="text" autofocus placeholder="Passcode"
               style="width:100%;font-size:16px;padding:12px;border-radius:10px;
                      background:var(--bg-input);border:1px solid var(--border);color:var(--text)" />
      </div>
      <button class="btn primary block" type="submit">Unlock</button>
    </form>
  </div>
</body>
</html>
"""


def login_page(message: str = "Enter the passcode to use this app.", status: int = 200) -> HTMLResponse:
    return HTMLResponse(LOGIN_PAGE.replace("__MESSAGE__", message), status_code=status)


def do_login(request: Request, passcode: str) -> Response:
    key = _client_key(request)
    if _throttled(key):
        return login_page("Too many attempts. Wait a few minutes and try again.", status=429)

    if not hmac.compare_digest(passcode.strip(), config.PASSCODE):
        _record_failure(key)
        return login_page("That passcode didn't match. Try again.", status=401)

    _failures.pop(key, None)
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        COOKIE_NAME,
        expected_token(),
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
        # Only mark Secure when actually on https, or the browser drops
        # the cookie on a plain-http LAN address and you can never log in.
        secure=request.url.scheme == "https",
        path="/",
    )
    return response
