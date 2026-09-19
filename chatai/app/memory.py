"""Long-term memory: when a chat's history grows past a token budget,
summarize the oldest chunk into chat.memory_summary via the same LLM,
then drop those messages from what gets sent as raw history (they stay
on disk in full, only the prompt sent to the model is shortened)."""
from __future__ import annotations

from .models import ChatSession, GenerationSettings
from .providers.base import Provider
from .tokens import estimate_tokens

SUMMARY_INSTRUCTION = (
    "Summarize the key facts, events, and emotional beats of the "
    "conversation so far in 4-8 concise sentences, written in third "
    "person, so they can be used as background memory for continuing "
    "the roleplay. Do not include meta-commentary, only the summary."
)


async def maybe_summarize(
    provider: Provider,
    chat: ChatSession,
    trigger_tokens: int,
    keep_recent: int = 8,
) -> bool:
    """Returns True if chat.memory_summary was updated."""
    total = sum(estimate_tokens(m.text()) for m in chat.messages)
    if total <= trigger_tokens or len(chat.messages) <= keep_recent:
        return False

    to_summarize = chat.messages[:-keep_recent]
    if not to_summarize:
        return False

    transcript = "\n".join(f"{m.role}: {m.text()}" for m in to_summarize)
    messages = [
        {"role": "system", "content": SUMMARY_INSTRUCTION},
        {"role": "user", "content": transcript},
    ]
    if chat.memory_summary:
        messages.insert(1, {
            "role": "system",
            "content": f"Existing memory summary to update/extend:\n{chat.memory_summary}",
        })

    summary_settings = GenerationSettings(temperature=0.3, max_tokens=300)
    summary = await provider.chat_once(messages, summary_settings)
    chat.memory_summary = summary.strip()
    # Keep only the most recent messages as raw history going forward.
    chat.messages = chat.messages[-keep_recent:]
    return True
