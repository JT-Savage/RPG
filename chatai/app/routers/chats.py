from __future__ import annotations

import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import config, storage
from ..models import ChatSession, Character, Message, Persona

router = APIRouter(prefix="/api/chats", tags=["chats"])


class CreateChatRequest(BaseModel):
    character_id: str
    persona_id: str | None = None


class MessageContent(BaseModel):
    content: str


class SwipeRequest(BaseModel):
    direction: str  # "prev" | "next"


def _summary(chat: ChatSession) -> dict:
    last = chat.messages[-1].text() if chat.messages else ""
    return {
        "id": chat.id,
        "character_id": chat.character_id,
        "persona_id": chat.persona_id,
        "title": chat.title,
        "updated_at": chat.updated_at,
        "last_message": last[:120],
        "message_count": len(chat.messages),
    }


@router.get("")
def list_chats() -> list[dict]:
    chats = storage.load_all(ChatSession, config.CHATS_DIR)
    chats.sort(key=lambda c: c.updated_at, reverse=True)
    return [_summary(c) for c in chats]


@router.post("")
def create_chat(req: CreateChatRequest) -> ChatSession:
    character = storage.load(Character, config.CHARACTERS_DIR, req.character_id)
    if not character:
        raise HTTPException(404, "Character not found")
    if req.persona_id and not storage.load(Persona, config.PERSONAS_DIR, req.persona_id):
        raise HTTPException(404, "Persona not found")

    chat = ChatSession(
        character_id=req.character_id,
        persona_id=req.persona_id,
        title=character.name,
    )
    if character.first_mes:
        chat.messages.append(Message(role="assistant", content=character.first_mes))
    storage.save(chat, config.CHATS_DIR)
    return chat


@router.get("/{chat_id}")
def get_chat(chat_id: str) -> ChatSession:
    chat = storage.load(ChatSession, config.CHATS_DIR, chat_id)
    if not chat:
        raise HTTPException(404, "Chat not found")
    return chat


@router.delete("/{chat_id}")
def delete_chat(chat_id: str) -> dict:
    if not storage.delete(config.CHATS_DIR, chat_id):
        raise HTTPException(404, "Chat not found")
    return {"deleted": True}


@router.post("/{chat_id}/messages")
def add_message(chat_id: str, body: MessageContent) -> ChatSession:
    chat = storage.load(ChatSession, config.CHATS_DIR, chat_id)
    if not chat:
        raise HTTPException(404, "Chat not found")
    chat.messages.append(Message(role="user", content=body.content))
    chat.updated_at = time.time()
    storage.save(chat, config.CHATS_DIR)
    return chat


@router.put("/{chat_id}/messages/{msg_id}")
def edit_message(chat_id: str, msg_id: str, body: MessageContent) -> ChatSession:
    chat = storage.load(ChatSession, config.CHATS_DIR, chat_id)
    if not chat:
        raise HTTPException(404, "Chat not found")
    for m in chat.messages:
        if m.id == msg_id:
            if m.role == "assistant" and m.swipes:
                m.swipes[m.active_swipe] = body.content
            else:
                m.content = body.content
            break
    else:
        raise HTTPException(404, "Message not found")
    chat.updated_at = time.time()
    storage.save(chat, config.CHATS_DIR)
    return chat


@router.delete("/{chat_id}/messages/{msg_id}")
def delete_message(chat_id: str, msg_id: str) -> ChatSession:
    chat = storage.load(ChatSession, config.CHATS_DIR, chat_id)
    if not chat:
        raise HTTPException(404, "Chat not found")
    before = len(chat.messages)
    chat.messages = [m for m in chat.messages if m.id != msg_id]
    if len(chat.messages) == before:
        raise HTTPException(404, "Message not found")
    chat.updated_at = time.time()
    storage.save(chat, config.CHATS_DIR)
    return chat


@router.post("/{chat_id}/swipe")
def swipe(chat_id: str, body: SwipeRequest) -> ChatSession:
    chat = storage.load(ChatSession, config.CHATS_DIR, chat_id)
    if not chat:
        raise HTTPException(404, "Chat not found")
    if not chat.messages or chat.messages[-1].role != "assistant":
        raise HTTPException(400, "Last message is not an assistant message")
    last = chat.messages[-1]
    if not last.swipes:
        raise HTTPException(400, "No swipes available")
    if body.direction == "next":
        last.active_swipe = min(last.active_swipe + 1, len(last.swipes) - 1)
    else:
        last.active_swipe = max(last.active_swipe - 1, 0)
    storage.save(chat, config.CHATS_DIR)
    return chat
