import base64
import json
import struct
import zlib

from app.card_io import parse_card_json, parse_card_png, to_export_dict


V2_CARD = {
    "spec": "chara_card_v2",
    "data": {
        "name": "Imported",
        "description": "A test character.",
        "first_mes": "Hello!",
        "character_book": {"entries": [{"keys": ["x"], "content": "y"}]},
    },
}


def test_parse_card_json_v2():
    char = parse_card_json(json.dumps(V2_CARD).encode())
    assert char.name == "Imported"
    assert char.first_mes == "Hello!"
    assert char.character_book[0].keys == ["x"]


def test_parse_card_json_v1_flat():
    flat = {"name": "FlatCard", "description": "flat desc", "first_mes": "hi"}
    char = parse_card_json(json.dumps(flat).encode())
    assert char.name == "FlatCard"


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def _make_test_png(card: dict) -> bytes:
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    idat = zlib.compress(b"\x00\xff\x00\x00")
    payload = base64.b64encode(json.dumps(card).encode()).decode()
    text_chunk = b"chara\x00" + payload.encode("latin-1")
    return (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", ihdr)
        + _png_chunk(b"tEXt", text_chunk)
        + _png_chunk(b"IDAT", idat)
        + _png_chunk(b"IEND", b"")
    )


def test_parse_card_png():
    png_bytes = _make_test_png(V2_CARD)
    char = parse_card_png(png_bytes)
    assert char.name == "Imported"


def test_export_roundtrips_through_import():
    char = parse_card_json(json.dumps(V2_CARD).encode())
    exported = to_export_dict(char)
    reimported = parse_card_json(json.dumps(exported).encode())
    assert reimported.name == char.name
    assert reimported.first_mes == char.first_mes
