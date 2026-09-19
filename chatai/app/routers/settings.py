from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import storage
from ..models import Settings
from ..providers import get_provider

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("")
def get_settings() -> Settings:
    return storage.load_settings()


@router.put("")
def update_settings(settings: Settings) -> Settings:
    storage.save_settings(settings)
    return settings


@router.get("/models")
async def list_models() -> dict:
    settings = storage.load_settings()
    provider = get_provider(settings.provider)
    try:
        models = await provider.list_models()
    except Exception as exc:
        raise HTTPException(
            502,
            f"Could not reach model server at {settings.provider.base_url}: {exc}",
        ) from exc
    return {"models": models}
