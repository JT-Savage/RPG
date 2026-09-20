"""The passcode gate that makes LAN exposure (i.e. phone access) safe."""
import pytest
from fastapi.testclient import TestClient

from app import auth, config
from app.main import app


@pytest.fixture
def locked(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "PASSCODE", "open-sesame")
    monkeypatch.setattr(config, "SECRET_FILE", tmp_path / "secret")
    auth._failures.clear()
    yield
    auth._failures.clear()


def test_open_by_default(monkeypatch):
    monkeypatch.setattr(config, "PASSCODE", "")
    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/api/characters").status_code == 200


def test_pages_redirect_to_login_when_locked(locked):
    with TestClient(app) as client:
        res = client.get("/", follow_redirects=False)
        assert res.status_code == 303
        assert res.headers["location"] == "/login"


def test_api_returns_401_when_locked(locked):
    with TestClient(app) as client:
        res = client.get("/api/characters")
        assert res.status_code == 401


def test_login_assets_stay_reachable_when_locked(locked):
    """The login page needs its stylesheet, and an installed app still
    needs the manifest/worker to boot far enough to show it."""
    with TestClient(app) as client:
        for path in ("/login", "/static/style.css", "/manifest.webmanifest",
                     "/sw.js", "/health"):
            assert client.get(path).status_code == 200, path


def test_wrong_passcode_is_rejected(locked):
    with TestClient(app) as client:
        res = client.post("/login", data={"passcode": "nope"}, follow_redirects=False)
        assert res.status_code == 401
        assert auth.COOKIE_NAME not in res.cookies
        assert client.get("/", follow_redirects=False).status_code == 303


def test_correct_passcode_unlocks_and_persists(locked):
    with TestClient(app) as client:
        res = client.post("/login", data={"passcode": "open-sesame"}, follow_redirects=False)
        assert res.status_code == 303
        assert res.headers["location"] == "/"
        assert auth.COOKIE_NAME in res.cookies

        # The cookie is carried by the client from here on.
        assert client.get("/").status_code == 200
        assert client.get("/api/characters").status_code == 200


def test_login_cookie_is_not_marked_secure_over_plain_http(locked):
    """A Secure cookie would be dropped on http://192.168.x.x, locking
    the phone out of its own server."""
    with TestClient(app) as client:
        res = client.post("/login", data={"passcode": "open-sesame"}, follow_redirects=False)
        assert "secure" not in res.headers["set-cookie"].lower()


def test_repeated_failures_are_throttled(locked):
    with TestClient(app) as client:
        for _ in range(auth._MAX_FAILURES):
            client.post("/login", data={"passcode": "nope"}, follow_redirects=False)
        res = client.post("/login", data={"passcode": "open-sesame"}, follow_redirects=False)
        assert res.status_code == 429
