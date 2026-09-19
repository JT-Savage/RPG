"""Keyword-triggered lorebook / world-info injection (SillyTavern-style)."""
from __future__ import annotations

from .models import LoreEntry


def matching_entries(entries: list[LoreEntry], recent_text: str, max_entries: int = 5) -> list[str]:
    """Return the .content of lore entries whose keys appear in recent_text."""
    if not entries or not recent_text:
        return []
    haystack_lower = recent_text.lower()
    hits: list[str] = []
    for entry in entries:
        if not entry.enabled or not entry.content:
            continue
        for key in entry.keys:
            if not key:
                continue
            needle = key if entry.case_sensitive else key.lower()
            haystack = recent_text if entry.case_sensitive else haystack_lower
            if needle in haystack:
                hits.append(entry.content)
                break
        if len(hits) >= max_entries:
            break
    return hits
