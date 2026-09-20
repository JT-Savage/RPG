"""The app has to be installable to the home screen, so the PWA plumbing
(manifest, service worker, icons) is part of the contract, not decoration."""
import json
import struct
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import config
from app.main import app

client = TestClient(app)
WEB = config.WEB_DIR


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{path} is not a PNG"
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def test_manifest_is_served_as_a_manifest():
    res = client.get("/manifest.webmanifest")
    assert res.status_code == 200
    assert "manifest" in res.headers["content-type"]

    manifest = json.loads(res.text)
    assert manifest["display"] == "standalone"
    assert manifest["start_url"].startswith("/")
    assert manifest["scope"] == "/"


def test_manifest_icons_exist_at_their_declared_sizes():
    manifest = json.loads((WEB / "manifest.webmanifest").read_text())
    for icon in manifest["icons"]:
        path = WEB / icon["src"].lstrip("/")
        assert path.exists(), f"missing icon {icon['src']}"
        declared = tuple(int(n) for n in icon["sizes"].split("x"))
        assert png_size(path) == declared


def test_manifest_has_a_maskable_icon():
    manifest = json.loads((WEB / "manifest.webmanifest").read_text())
    assert any("maskable" in (i.get("purpose") or "") for i in manifest["icons"])


def test_service_worker_is_served_from_the_root_scope():
    res = client.get("/sw.js")
    assert res.status_code == 200
    assert "javascript" in res.headers["content-type"]
    # A worker cached by the browser would pin an old app version.
    assert res.headers["cache-control"] == "no-cache"
    assert res.headers["service-worker-allowed"] == "/"


def test_service_worker_precaches_only_files_that_exist():
    source = (WEB / "sw.js").read_text()
    listed = [line.strip().strip('",')
              for line in source.split("const SHELL_ASSETS = [")[1].split("];")[0].splitlines()
              if line.strip().startswith('"')]
    assert "/" in listed
    for asset in listed:
        if asset == "/":
            continue
        # Root-level files live in web/, everything else under web/static.
        assert (WEB / asset.lstrip("/")).exists(), f"precached but missing: {asset}"


def test_service_worker_never_caches_the_api():
    source = (WEB / "sw.js").read_text()
    assert 'url.pathname.startsWith("/api/")' in source
    assert "text/event-stream" in source  # streamed replies must pass through


def test_offline_page_is_served():
    res = client.get("/offline.html")
    assert res.status_code == 200
    assert "Can't reach your server" in res.text


@pytest.mark.parametrize("path", ["/favicon.ico", "/apple-touch-icon.png",
                                  "/apple-touch-icon-precomposed.png"])
def test_icon_shortcuts(path):
    res = client.get(path)
    assert res.status_code == 200
    assert res.headers["content-type"] == "image/png"


def test_index_declares_the_ios_home_screen_tags():
    html = client.get("/").text
    assert '<link rel="manifest" href="/manifest.webmanifest"' in html
    assert 'name="apple-mobile-web-app-capable" content="yes"' in html
    assert 'rel="apple-touch-icon"' in html
    # viewport-fit=cover is what lets the CSS safe-area insets do anything.
    assert "viewport-fit=cover" in html
