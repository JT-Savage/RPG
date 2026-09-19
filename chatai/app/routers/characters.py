from __future__ import annotations

import shutil

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from .. import config, storage
from ..card_io import parse_card_json, parse_card_png, to_export_dict
from ..models import Character

router = APIRouter(prefix="/api/characters", tags=["characters"])


@router.get("")
def list_characters() -> list[Character]:
    return storage.load_all(Character, config.CHARACTERS_DIR)


@router.post("")
def create_character(character: Character) -> Character:
    storage.save(character, config.CHARACTERS_DIR)
    return character


@router.get("/{char_id}")
def get_character(char_id: str) -> Character:
    char = storage.load(Character, config.CHARACTERS_DIR, char_id)
    if not char:
        raise HTTPException(404, "Character not found")
    return char


@router.put("/{char_id}")
def update_character(char_id: str, character: Character) -> Character:
    existing = storage.load(Character, config.CHARACTERS_DIR, char_id)
    if not existing:
        raise HTTPException(404, "Character not found")
    character.id = char_id
    character.created_at = existing.created_at
    import time
    character.updated_at = time.time()
    storage.save(character, config.CHARACTERS_DIR)
    return character


@router.delete("/{char_id}")
def delete_character(char_id: str) -> dict:
    ok = storage.delete(config.CHARACTERS_DIR, char_id)
    avatar_dir = config.CHARACTERS_DIR / char_id
    if avatar_dir.exists():
        shutil.rmtree(avatar_dir, ignore_errors=True)
    if not ok:
        raise HTTPException(404, "Character not found")
    return {"deleted": True}


@router.post("/import")
async def import_character(file: UploadFile) -> Character:
    raw = await file.read()
    filename = (file.filename or "").lower()
    try:
        if filename.endswith(".png"):
            character = parse_card_png(raw)
        else:
            character = parse_card_json(raw)
    except Exception as exc:
        raise HTTPException(400, f"Could not parse character card: {exc}") from exc
    storage.save(character, config.CHARACTERS_DIR)
    return character


@router.get("/{char_id}/export")
def export_character(char_id: str) -> JSONResponse:
    char = storage.load(Character, config.CHARACTERS_DIR, char_id)
    if not char:
        raise HTTPException(404, "Character not found")
    return JSONResponse(
        content=to_export_dict(char),
        headers={"Content-Disposition": f'attachment; filename="{char.name}.json"'},
    )


@router.post("/{char_id}/avatar")
async def upload_avatar(char_id: str, file: UploadFile) -> Character:
    char = storage.load(Character, config.CHARACTERS_DIR, char_id)
    if not char:
        raise HTTPException(404, "Character not found")
    ext = (file.filename or "avatar.png").rsplit(".", 1)[-1].lower()
    if ext not in ("png", "jpg", "jpeg", "webp", "gif"):
        ext = "png"
    char_dir = config.CHARACTERS_DIR / char_id
    char_dir.mkdir(parents=True, exist_ok=True)
    dest = char_dir / f"avatar.{ext}"
    raw = await file.read()
    dest.write_bytes(raw)
    char.avatar = f"{char_id}/avatar.{ext}"
    storage.save(char, config.CHARACTERS_DIR)
    return char
