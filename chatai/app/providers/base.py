"""Provider interface. A provider is any local (or, if you choose, remote)
model server speaking either the Ollama API or an OpenAI-compatible API."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from ..models import GenerationSettings


class Provider(ABC):
    def __init__(self, base_url: str, api_key: str = "", model: str = ""):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def stream_chat(
        self, messages: list[dict], settings: GenerationSettings
    ) -> AsyncIterator[str]:
        """Yield text deltas as they are generated."""
        ...

    async def chat_once(self, messages: list[dict], settings: GenerationSettings) -> str:
        """Non-streaming convenience wrapper, used for memory summarization."""
        out = []
        async for delta in self.stream_chat(messages, settings):
            out.append(delta)
        return "".join(out)

    @abstractmethod
    async def list_models(self) -> list[str]:
        ...
