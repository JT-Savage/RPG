"""Streaming generation endpoints (Server-Sent Events)."""
from __future__ import annotations

import json
import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .. import config, storage
from ..memory import maybe_summarize
from ..models import ChatSession, Character, Message, Persona
from ..prompt import build_messages
from ..providers import get_provider

router = APIRouter(prefix="/api/chats", tags=["generate"])


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event)}\n\n"


async def _run_generation(chat_id: str, mode: str):
    chat = storage.load(ChatSession, config.CHATS_DIR, chat_id)
    if not chat:
        yield _sse({"error": "Chat not found"})
        return
    character = storage.load(Character, config.CHARACTERS_DIR, chat.character_id)
    if not character:
        yield _sse({"error": "Character not found"})
        return
    persona = storage.load(Persona, config.PERSONAS_DIR, chat.persona_id) if chat.persona_id else None

    settings = storage.load_settings()
    provider = get_provider(settings.provider)
    if not settings.provider.model:
        yield _sse({"error": "No model selected. Open Settings and choose a model."})
        return

    if mode == "regenerate":
        if not chat.messages or chat.messages[-1].role != "assistant":
            yield _sse({"error": "Nothing to regenerate"})
            return
    else:
        if not chat.messages or chat.messages[-1].role != "user":
            yield _sse({"error": "Add a message before generating a reply"})
            return

    if settings.memory_enabled:
        try:
            # Summarize everything except the very last message (which, on
            # regenerate, is the assistant turn we're about to replace).
            tail = chat.model_copy(deep=True)
            held = tail.messages.pop() if mode == "regenerate" else None
            changed = await maybe_summarize(provider, tail, settings.memory_trigger_tokens)
            if changed:
                chat.memory_summary = tail.memory_summary
                chat.messages = tail.messages + ([held] if held is not None else [])
        except Exception:
            pass  # memory is best-effort; never block generation on it

    # Build the prompt as if the message we're about to produce doesn't exist yet.
    prompt_source = chat
    target = None
    if mode == "regenerate":
        prompt_source = chat.model_copy(deep=True)
        target = prompt_source.messages.pop()

    messages = build_messages(character, persona, prompt_source, settings.generation)

    collected: list[str] = []
    try:
        async for delta in provider.stream_chat(messages, settings.generation):
            collected.append(delta)
            yield _sse({"delta": delta})
    except Exception as exc:
        yield _sse({"error": f"Generation failed: {exc}"})
        return

    full_text = "".join(collected).strip()
    if mode == "regenerate" and target is not None:
        target.swipes.append(full_text)
        target.active_swipe = len(target.swipes) - 1
        chat.messages[-1] = target
    else:
        chat.messages.append(Message(role="assistant", content=full_text, swipes=[full_text]))

    chat.updated_at = time.time()
    storage.save(chat, config.CHATS_DIR)

    yield _sse({"done": True, "message": json.loads(chat.messages[-1].model_dump_json())})


@router.get("/{chat_id}/generate")
async def generate(chat_id: str):
    return StreamingResponse(_run_generation(chat_id, "generate"), media_type="text/event-stream")


@router.get("/{chat_id}/regenerate")
async def regenerate(chat_id: str):
    return StreamingResponse(_run_generation(chat_id, "regenerate"), media_type="text/event-stream")
