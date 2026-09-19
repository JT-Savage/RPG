"""
Cheap token estimation.

We don't want a hard dependency on tiktoken (it's a large binary wheel
and the exact tokenizer varies per local model anyway), so we use a
simple heuristic: ~4 characters per token, which is close enough for
budgeting context windows against local GGUF/transformers models.
"""
from __future__ import annotations


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)


def estimate_messages_tokens(messages: list[dict]) -> int:
    return sum(estimate_tokens(m.get("content", "")) for m in messages) + len(messages) * 4
