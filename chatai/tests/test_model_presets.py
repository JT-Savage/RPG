"""The suggested-model list is data the UI renders verbatim, so it has to
stay well-formed: every entry needs something to pull (or somewhere to
look), a size, and a reason to pick it."""
import json

from fastapi.testclient import TestClient

from app import config
from app.main import app

client = TestClient(app)
CATALOGUE = json.loads((config.WEB_DIR / "static" / "models.json").read_text())


def all_presets():
    for tier in CATALOGUE["tiers"]:
        for preset in tier["presets"]:
            yield tier, preset


def test_catalogue_is_served():
    res = client.get("/static/models.json")
    assert res.status_code == 200
    assert res.json()["tiers"]


def test_tiers_are_labelled_and_populated():
    assert CATALOGUE["tiers"]
    for tier in CATALOGUE["tiers"]:
        assert tier["label"].strip()
        assert tier["presets"], f"empty tier: {tier['label']}"


def test_every_preset_is_complete():
    for _, preset in all_presets():
        assert preset["name"].strip()
        assert preset["vram"].strip()
        assert preset["flavor"].strip()
        # Either a concrete pull command, or a pointer to go look.
        assert preset.get("pull") or preset.get("search"), preset["name"]


def test_pull_tags_are_unique_and_tagged():
    pulls = [p["pull"] for _, p in all_presets() if p.get("pull")]
    assert len(pulls) == len(set(pulls)), "duplicate pull target"
    for pull in pulls:
        # An explicit size tag keeps Ollama from silently grabbing a
        # different variant than the one the size estimate describes.
        assert ":" in pull, f"{pull} has no size tag"


def test_search_links_point_at_the_library():
    for _, preset in all_presets():
        if preset.get("search"):
            assert preset["search"].startswith("https://")


def test_caveats_are_present():
    # The UI shows these verbatim; without them the sizes and names read
    # as more authoritative than they are.
    assert CATALOGUE["quant_note"].strip()
    assert CATALOGUE["caveat"].strip()
