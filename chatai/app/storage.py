"""
Flat-file JSON persistence.

No database, no external services. Every record is one JSON file on
local disk under app.config.DATA_DIR. Writes are atomic (write to a
temp file, then os.replace) so a crash mid-write can't corrupt a record.
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel

from . import config

T = TypeVar("T", bound=BaseModel)

_lock = threading.Lock()


def _atomic_write(path: Path, data: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with _lock:
        tmp.write_text(data, encoding="utf-8")
        os.replace(tmp, path)


def save(model: BaseModel, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{model.id}.json"
    _atomic_write(path, model.model_dump_json(indent=2))


def load(cls: Type[T], directory: Path, id_: str) -> T | None:
    path = directory / f"{id_}.json"
    if not path.exists():
        return None
    return cls.model_validate_json(path.read_text(encoding="utf-8"))


def load_all(cls: Type[T], directory: Path) -> list[T]:
    if not directory.exists():
        return []
    out = []
    for path in sorted(directory.glob("*.json")):
        try:
            out.append(cls.model_validate_json(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return out


def delete(directory: Path, id_: str) -> bool:
    path = directory / f"{id_}.json"
    if path.exists():
        path.unlink()
        return True
    return False


def load_settings():
    from .models import Settings
    if config.SETTINGS_FILE.exists():
        try:
            return Settings.model_validate_json(config.SETTINGS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    s = Settings()
    save_settings(s)
    return s


def save_settings(settings) -> None:
    _atomic_write(config.SETTINGS_FILE, settings.model_dump_json(indent=2))
