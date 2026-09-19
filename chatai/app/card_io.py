"""
Import/export of SillyTavern/TavernAI-style character cards.

Supports:
  * .json  — the "v2" character card spec (fields nested under
             {"spec": "chara_card_v2", "data": {...}}) as well as the
             older flat v1 layout, so cards exported from most existing
             character-chat tools can be dropped in directly.
  * .png   — cards with the JSON embedded as base64 in a tEXt/zTXt
             "chara" chunk (the de-facto standard used by TavernAI/
             SillyTavern/character hubs). We only need stdlib (zlib +
             struct) to read PNG chunks, no imaging library required.

Export writes plain JSON (v2-shaped). Re-embedding into a PNG on export
is intentionally not implemented — the JSON export is the source of
truth and can be re-imported here or into SillyTavern directly.
"""
from __future__ import annotations

import base64
import json
import struct
import zlib

from .models import Character, LoreEntry


def _read_png_text_chunks(data: bytes) -> dict[str, str]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG file")
    out: dict[str, str] = {}
    pos = 8
    length = len(data)
    while pos + 8 <= length:
        (chunk_len,) = struct.unpack(">I", data[pos:pos + 4])
        chunk_type = data[pos + 4:pos + 8].decode("ascii", errors="replace")
        chunk_data = data[pos + 8:pos + 8 + chunk_len]
        if chunk_type == "tEXt":
            if b"\x00" in chunk_data:
                key, _, value = chunk_data.partition(b"\x00")
                out[key.decode("latin-1")] = value.decode("latin-1")
        elif chunk_type == "zTXt":
            if b"\x00" in chunk_data:
                key, _, rest = chunk_data.partition(b"\x00")
                if rest[:1] == b"\x00":  # compression method 0
                    try:
                        value = zlib.decompress(rest[1:]).decode("utf-8", errors="replace")
                        out[key.decode("latin-1")] = value
                    except zlib.error:
                        pass
        pos += 8 + chunk_len + 4  # data + CRC
        if chunk_type == "IEND":
            break
    return out


def _normalize_card_dict(raw: dict) -> Character:
    data = raw.get("data", raw)  # v2 nests under "data"; v1 is flat

    book_entries: list[LoreEntry] = []
    book = data.get("character_book") or raw.get("character_book")
    if book and isinstance(book, dict):
        for entry in book.get("entries", []) or []:
            if isinstance(entry, dict):
                keys = entry.get("keys") or entry.get("key") or []
                if isinstance(keys, str):
                    keys = [keys]
                book_entries.append(LoreEntry(
                    keys=keys,
                    content=entry.get("content", ""),
                    enabled=not entry.get("disable", False),
                    case_sensitive=bool(entry.get("case_sensitive", False)),
                ))

    alt_greetings = data.get("alternate_greetings") or []

    return Character(
        name=data.get("name") or "Unnamed",
        description=data.get("description", ""),
        personality=data.get("personality", ""),
        scenario=data.get("scenario", ""),
        first_mes=data.get("first_mes", ""),
        alternate_greetings=list(alt_greetings),
        mes_example=data.get("mes_example", ""),
        system_prompt=data.get("system_prompt", ""),
        post_history_instructions=data.get("post_history_instructions", ""),
        creator_notes=data.get("creator_notes", ""),
        tags=list(data.get("tags") or []),
        character_book=book_entries,
    )


def parse_card_json(raw_bytes: bytes) -> Character:
    raw = json.loads(raw_bytes.decode("utf-8"))
    return _normalize_card_dict(raw)


def parse_card_png(raw_bytes: bytes) -> Character:
    chunks = _read_png_text_chunks(raw_bytes)
    payload = chunks.get("chara") or chunks.get("ccv3")
    if not payload:
        raise ValueError("No embedded character data found in PNG (missing 'chara' chunk)")
    decoded = base64.b64decode(payload)
    raw = json.loads(decoded.decode("utf-8"))
    return _normalize_card_dict(raw)


def to_export_dict(character: Character) -> dict:
    return {
        "spec": "chara_card_v2",
        "spec_version": "2.0",
        "data": {
            "name": character.name,
            "description": character.description,
            "personality": character.personality,
            "scenario": character.scenario,
            "first_mes": character.first_mes,
            "alternate_greetings": character.alternate_greetings,
            "mes_example": character.mes_example,
            "system_prompt": character.system_prompt,
            "post_history_instructions": character.post_history_instructions,
            "creator_notes": character.creator_notes,
            "tags": character.tags,
            "character_book": {
                "entries": [
                    {
                        "keys": e.keys,
                        "content": e.content,
                        "disable": not e.enabled,
                        "case_sensitive": e.case_sensitive,
                    }
                    for e in character.character_book
                ]
            },
        },
    }
