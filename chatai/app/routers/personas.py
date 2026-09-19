from __future__ import annotations

import time

from fastapi import APIRouter, HTTPException

from .. import config, storage
from ..models import Persona

router = APIRouter(prefix="/api/personas", tags=["personas"])


@router.get("")
def list_personas() -> list[Persona]:
    return storage.load_all(Persona, config.PERSONAS_DIR)


@router.post("")
def create_persona(persona: Persona) -> Persona:
    storage.save(persona, config.PERSONAS_DIR)
    return persona


@router.put("/{persona_id}")
def update_persona(persona_id: str, persona: Persona) -> Persona:
    existing = storage.load(Persona, config.PERSONAS_DIR, persona_id)
    if not existing:
        raise HTTPException(404, "Persona not found")
    persona.id = persona_id
    persona.created_at = existing.created_at
    persona.updated_at = time.time()
    storage.save(persona, config.PERSONAS_DIR)
    return persona


@router.delete("/{persona_id}")
def delete_persona(persona_id: str) -> dict:
    if not storage.delete(config.PERSONAS_DIR, persona_id):
        raise HTTPException(404, "Persona not found")
    return {"deleted": True}
