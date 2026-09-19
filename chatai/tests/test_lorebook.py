from app.lorebook import matching_entries
from app.models import LoreEntry


def test_matches_case_insensitive_key():
    entries = [LoreEntry(keys=["sword"], content="A magic sword.")]
    assert matching_entries(entries, "I see a SWORD on the table.") == ["A magic sword."]


def test_no_match_returns_empty():
    entries = [LoreEntry(keys=["dragon"], content="Beware the dragon.")]
    assert matching_entries(entries, "Just a quiet walk in the park.") == []


def test_disabled_entry_is_skipped():
    entries = [LoreEntry(keys=["sword"], content="Ignored.", enabled=False)]
    assert matching_entries(entries, "a sword") == []


def test_respects_max_entries():
    entries = [LoreEntry(keys=[f"key{i}"], content=f"content{i}") for i in range(10)]
    text = " ".join(f"key{i}" for i in range(10))
    assert len(matching_entries(entries, text, max_entries=3)) == 3
