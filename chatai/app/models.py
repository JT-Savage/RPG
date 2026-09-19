"""Pydantic schemas shared across the app."""
from __future__ import annotations

import time
import uuid
from typing import Literal, Optional

from pydantic import BaseModel, Field


def new_id() -> str:
    return uuid.uuid4().hex[:12]


def now() -> float:
    return time.time()


class LoreEntry(BaseModel):
    """A single SillyTavern-style lorebook / world-info entry."""
    keys: list[str] = Field(default_factory=list)
    content: str = ""
    enabled: bool = True
    case_sensitive: bool = False


class Character(BaseModel):
    """SillyTavern v2 card fields, minus the embedded PNG art."""
    id: str = Field(default_factory=new_id)
    name: str
    description: str = ""
    personality: str = ""
    scenario: str = ""
    first_mes: str = ""
    alternate_greetings: list[str] = Field(default_factory=list)
    mes_example: str = ""
    system_prompt: str = ""
    post_history_instructions: str = ""
    creator_notes: str = ""
    tags: list[str] = Field(default_factory=list)
    avatar: Optional[str] = None  # relative path under data/characters/<id>/avatar.*
    character_book: list[LoreEntry] = Field(default_factory=list)
    created_at: float = Field(default_factory=now)
    updated_at: float = Field(default_factory=now)


class Persona(BaseModel):
    """Who the user is playing as."""
    id: str = Field(default_factory=new_id)
    name: str = "User"
    description: str = ""
    avatar: Optional[str] = None
    created_at: float = Field(default_factory=now)
    updated_at: float = Field(default_factory=now)


class Message(BaseModel):
    id: str = Field(default_factory=new_id)
    role: Literal["user", "assistant", "system"]
    content: str
    swipes: list[str] = Field(default_factory=list)
    active_swipe: int = 0
    created_at: float = Field(default_factory=now)

    def text(self) -> str:
        if self.role == "assistant" and self.swipes:
            idx = max(0, min(self.active_swipe, len(self.swipes) - 1))
            return self.swipes[idx]
        return self.content


class GenerationSettings(BaseModel):
    temperature: float = 0.9
    top_p: float = 0.95
    top_k: int = 40
    repeat_penalty: float = 1.1
    max_tokens: int = 400
    context_length: int = 8192
    stop: list[str] = Field(default_factory=list)


class ProviderSettings(BaseModel):
    """Which local model server to talk to, and how."""
    provider: Literal["ollama", "openai_compatible"] = "ollama"
    base_url: str = "http://127.0.0.1:11434"
    api_key: str = ""  # only sent to base_url; stored locally in data/settings.json
    model: str = ""


class Settings(BaseModel):
    provider: ProviderSettings = Field(default_factory=ProviderSettings)
    generation: GenerationSettings = Field(default_factory=GenerationSettings)
    memory_enabled: bool = True
    memory_trigger_tokens: int = 3000  # summarize once history exceeds this


class ChatSession(BaseModel):
    id: str = Field(default_factory=new_id)
    character_id: str
    persona_id: Optional[str] = None
    title: str = ""
    messages: list[Message] = Field(default_factory=list)
    memory_summary: str = ""
    created_at: float = Field(default_factory=now)
    updated_at: float = Field(default_factory=now)
