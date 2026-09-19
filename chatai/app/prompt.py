"""
Assembles the message list sent to the model from:
  system prompt (character.system_prompt, or a sane default)
  + persona description
  + character description / personality / scenario
  + lorebook entries triggered by recent conversation
  + memory summary of anything trimmed out of history
  + example dialogue (mes_example), as a scripted exchange
  + as much real chat history as fits the context budget
  + post_history_instructions (injected right before generation)
"""
from __future__ import annotations

from .lorebook import matching_entries
from .models import Character, ChatSession, GenerationSettings, Persona
from .tokens import estimate_tokens

DEFAULT_SYSTEM = (
    "You are role-playing as the character described below. Stay fully in "
    "character, write vivid and consistent responses, and never break the "
    "fourth wall or mention that you are an AI unless the character itself "
    "would say so."
)


def _char_block(character: Character) -> str:
    parts = [f"Name: {character.name}"]
    if character.description:
        parts.append(f"Description: {character.description}")
    if character.personality:
        parts.append(f"Personality: {character.personality}")
    if character.scenario:
        parts.append(f"Scenario: {character.scenario}")
    return "\n".join(parts)


def _persona_block(persona: Persona | None) -> str:
    if not persona:
        return ""
    parts = [f"The user is playing as: {persona.name}"]
    if persona.description:
        parts.append(persona.description)
    return "\n".join(parts)


def build_messages(
    character: Character,
    persona: Persona | None,
    chat: ChatSession,
    settings: GenerationSettings,
    reserve_for_reply: int | None = None,
) -> list[dict]:
    reserve = reserve_for_reply if reserve_for_reply is not None else settings.max_tokens
    budget = max(512, settings.context_length - reserve)

    system_text = character.system_prompt.strip() or DEFAULT_SYSTEM
    system_text += "\n\n" + _char_block(character)

    persona_text = _persona_block(persona)
    if persona_text:
        system_text += "\n\n" + persona_text

    recent_text = " ".join(m.text() for m in chat.messages[-6:])
    lore_hits = matching_entries(character.character_book, recent_text)
    if lore_hits:
        system_text += "\n\nWorld info:\n" + "\n".join(f"- {hit}" for hit in lore_hits)

    if chat.memory_summary:
        system_text += (
            "\n\nSummary of earlier events in this conversation (for continuity):\n"
            + chat.memory_summary
        )

    messages: list[dict] = [{"role": "system", "content": system_text}]

    if character.mes_example:
        messages.append({
            "role": "system",
            "content": "Example dialogue for tone/style reference:\n" + character.mes_example,
        })

    used = estimate_tokens(system_text) + estimate_tokens(character.mes_example)

    # Walk history backwards, keeping the most recent turns that fit budget.
    history_msgs: list[dict] = []
    for m in reversed(chat.messages):
        content = m.text()
        cost = estimate_tokens(content)
        if used + cost > budget and history_msgs:
            break
        used += cost
        history_msgs.append({"role": m.role, "content": content})
    history_msgs.reverse()
    messages.extend(history_msgs)

    if character.post_history_instructions:
        messages.append({"role": "system", "content": character.post_history_instructions})

    return messages


def trimmed_out_messages(chat: ChatSession, kept_from_end: int) -> list:
    """Messages that build_messages would drop from the *front* of history,
    given that `kept_from_end` most-recent messages were kept."""
    if kept_from_end >= len(chat.messages):
        return []
    return chat.messages[: len(chat.messages) - kept_from_end]
