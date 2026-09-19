"""Provider for a local Ollama server (https://ollama.com), the default
and easiest way to run an uncensored/roleplay-friendly model entirely
on your own machine: `ollama pull <model>` then this app talks to
http://127.0.0.1:11434 with nothing else required."""
from __future__ import annotations

import json
from collections.abc import AsyncIterator

import httpx

from ..models import GenerationSettings
from .base import Provider


class OllamaProvider(Provider):
    async def stream_chat(
        self, messages: list[dict], settings: GenerationSettings
    ) -> AsyncIterator[str]:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": settings.temperature,
                "top_p": settings.top_p,
                "top_k": settings.top_k,
                "repeat_penalty": settings.repeat_penalty,
                "num_predict": settings.max_tokens,
                "num_ctx": settings.context_length,
                "stop": settings.stop or None,
            },
        }
        url = f"{self.base_url}/api/chat"
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.strip():
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if obj.get("done"):
                        break
                    content = obj.get("message", {}).get("content", "")
                    if content:
                        yield content

    async def list_models(self) -> list[str]:
        url = f"{self.base_url}/api/tags"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
        return [m["name"] for m in data.get("models", [])]
