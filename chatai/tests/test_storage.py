from pathlib import Path

from app.models import Character
from app import storage


def test_save_load_roundtrip(tmp_path: Path):
    char = Character(name="Test Char", description="desc")
    storage.save(char, tmp_path)
    loaded = storage.load(Character, tmp_path, char.id)
    assert loaded is not None
    assert loaded.name == "Test Char"
    assert loaded.id == char.id


def test_load_missing_returns_none(tmp_path: Path):
    assert storage.load(Character, tmp_path, "doesnotexist") is None


def test_load_all_and_delete(tmp_path: Path):
    a = Character(name="A")
    b = Character(name="B")
    storage.save(a, tmp_path)
    storage.save(b, tmp_path)
    all_chars = storage.load_all(Character, tmp_path)
    assert {c.id for c in all_chars} == {a.id, b.id}

    assert storage.delete(tmp_path, a.id) is True
    assert storage.delete(tmp_path, a.id) is False
    remaining = storage.load_all(Character, tmp_path)
    assert {c.id for c in remaining} == {b.id}
