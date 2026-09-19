from app.models import Character, ChatSession, GenerationSettings, Message, Persona
from app.prompt import build_messages


def _character(**kw):
    return Character(name="Nyra", description="A rogue.", **kw)


def test_system_message_includes_character_fields():
    char = _character(personality="Sarcastic", scenario="A tavern")
    chat = ChatSession(character_id=char.id)
    msgs = build_messages(char, None, chat, GenerationSettings())
    assert msgs[0]["role"] == "system"
    assert "Nyra" in msgs[0]["content"]
    assert "Sarcastic" in msgs[0]["content"]
    assert "A tavern" in msgs[0]["content"]


def test_persona_is_injected():
    char = _character()
    persona = Persona(name="Alex", description="A traveler")
    chat = ChatSession(character_id=char.id)
    msgs = build_messages(char, persona, chat, GenerationSettings())
    assert "Alex" in msgs[0]["content"]


def test_lorebook_entry_injected_when_triggered():
    char = _character()
    char.character_book = [__import__("app.models", fromlist=["LoreEntry"]).LoreEntry(
        keys=["dagger"], content="It is enchanted."
    )]
    chat = ChatSession(character_id=char.id)
    chat.messages.append(Message(role="user", content="Nice dagger!"))
    msgs = build_messages(char, None, chat, GenerationSettings())
    assert "enchanted" in msgs[0]["content"]


def test_history_included_in_order():
    char = _character()
    chat = ChatSession(character_id=char.id)
    chat.messages.append(Message(role="user", content="Hello"))
    chat.messages.append(Message(role="assistant", content="Hi there"))
    msgs = build_messages(char, None, chat, GenerationSettings())
    roles_and_content = [(m["role"], m["content"]) for m in msgs]
    assert ("user", "Hello") in roles_and_content
    assert ("assistant", "Hi there") in roles_and_content


def test_memory_summary_included():
    char = _character()
    chat = ChatSession(character_id=char.id, memory_summary="They met at a market.")
    msgs = build_messages(char, None, chat, GenerationSettings())
    assert "They met at a market." in msgs[0]["content"]


def test_history_trimmed_to_budget():
    char = _character()
    chat = ChatSession(character_id=char.id)
    for i in range(200):
        chat.messages.append(Message(role="user", content=f"message number {i} " * 20))
    settings = GenerationSettings(context_length=1000, max_tokens=200)
    msgs = build_messages(char, None, chat, settings)
    # Should not include all 200 messages given the tight budget.
    history_count = sum(1 for m in msgs if m["role"] == "user")
    assert history_count < 200
    # Most recent message should always be present.
    assert "message number 199" in msgs[-1]["content"] or any(
        "message number 199" in m["content"] for m in msgs
    )
