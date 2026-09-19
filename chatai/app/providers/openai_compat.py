"""Provider for any OpenAI-compatible chat-completions endpoint.

This covers most local model servers people run for uncensored roleplay
chat (LM Studio, text-generation-webui's OpenAI extension, koboldcpp,
llama.cpp's `server` binary, vLLM) as well as, if you deliberately choose
to, a real hosted API such as OpenAI or OpenRouter. The base_url and
api_key are only ever sent to whatever base_url you configure yourself —
by default that's a localhost address, so nothing leaves your machine."""
from __future__ import annotations

import json
from collections.abc import AsyncIterator

import httpx

from ..models import GenerationSettings
from .base import Provider


class OpenAICompatibleProvider(Provider):
    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def stream_chat(
        self, messages: list[dict], settings: GenerationSettings
    ) -> AsyncIterator[str]:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "temperature": settings.temperature,
            "top_p": settings.top_p,
            "max_tokens": settings.max_tokens,
        }
        if settings.stop:
            payload["stop"] = settings.stop
        url = f"{self.base_url}/v1/chat/completions"
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST", url, json=payload, headers=self._headers()
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    line = line.strip()
                    if not line or not line.startswith("data:"):
                        continue
                    data = line[len("data:"):].strip()
                    if data == "[DONE]":
                        break
                    try:
                        obj = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    choices = obj.get("choices") or []
                    if not choices:
                        continue
                    delta = choices[0].get("delta", {}) or {}
                    content = delta.get("content", "")
                    if content:
                        yield content

    async def list_models(self) -> list[str]:
        url = f"{self.base_url}/v1/models"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=self._headers())
            resp.raise_for_status()
            data = resp.json()
        return [m["id"] for m in data.get("data", [])]
