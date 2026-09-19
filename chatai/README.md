# Private Character Chat

A self-hosted, character-based AI chat app you run entirely on your own
machine — the same idea as SpicyChat/character.ai-style apps, but with
no account, no cloud service, and no one else's server involved. It
talks to a **local** language model server that you install yourself,
and stores all characters, personas, and chat history as plain JSON
files on your own disk.

By default the app binds to `127.0.0.1` only (not reachable from the
network), stores data under `chatai/data/` (gitignored, never
committed), and makes zero outbound network calls on its own — the
only network traffic it generates is to whatever local model server
base URL *you* configure in Settings.

## What you get

- Character cards compatible with the SillyTavern/TavernAI v2 format —
  import existing `.json` or `.png` cards, or create your own from
  scratch in the built-in editor (description, personality, scenario,
  greeting, example dialogue, lorebook/world-info, avatar).
- User personas — define who *you* are in the roleplay, switch between
  several.
- Multiple chats per character, streamed responses, message editing,
  deletion, regenerate, and "swipe" between alternate replies.
- A lorebook engine: keyword-triggered world-info snippets get injected
  into the prompt automatically when relevant.
- Long-term memory: once a chat's history gets long, older turns are
  summarized by the model itself so the story keeps continuity without
  blowing the context window.
- Adjustable sampler settings (temperature, top-p, top-k, repetition
  penalty, max tokens, context length).
- Pluggable model backend: **Ollama** (default, easiest) or any
  **OpenAI-compatible** local server — LM Studio, llama.cpp's `server`,
  koboldcpp, text-generation-webui, vLLM. You could also point it at a
  hosted API if you explicitly choose to, but nothing here requires
  that, and doing so means your chats leave your machine.

## 1. Install a local model server

Pick one:

- **Ollama** (recommended, simplest): install from https://ollama.com,
  then pull a model, e.g.:
  ```
  ollama pull llama3.1
  ```
  or search for a roleplay/uncensored-tuned model on Ollama's library
  if you want something less restrictive for creative fiction.
- **LM Studio**: install it, download a GGUF model in-app, and start
  its local server (Developer tab → Start Server). Note the port shown
  (usually `1234`).
- **llama.cpp / koboldcpp / text-generation-webui / vLLM**: run their
  OpenAI-compatible server mode and note the base URL/port.

## 2. Run this app

```
cd chatai
./run.sh          # macOS/Linux
# or
.\run.ps1         # Windows PowerShell
```

This creates a virtual environment, installs the small set of Python
dependencies (FastAPI, uvicorn, httpx, pydantic — no ML libraries; the
actual model runs in the separate server from step 1), and starts the
app at **http://127.0.0.1:8765**.

Open that URL in a browser.

## 3. Configure it

Click the ⚙ Settings button:
- **Model backend**: "Ollama" if you used Ollama, otherwise
  "OpenAI-compatible server".
- **Base URL**: `http://127.0.0.1:11434` for Ollama, or whatever your
  server printed (LM Studio defaults to `http://127.0.0.1:1234`).
- Click **Refresh list** and pick your model.
- Adjust sampling settings if you like (the defaults are reasonable for
  most models).

## 4. Create a character and chat

Go to the **Characters** tab → **+ Character**, fill in the fields, and
click **Chat**. Or click **Import card** to load an existing
SillyTavern-style `.json`/`.png` card — including the example one in
`chatai/characters/example_luma.json`.

## Notes on privacy & responsible use

- This app does not phone home, does not use analytics, and has no
  account system. Your chats live only in `chatai/data/` on this
  machine.
- If you set the Base URL to a real hosted API instead of a local
  server, understand that your messages then go to that provider under
  their terms — that is a choice you make explicitly, not a default.
- Local models vary widely in what content they will produce. You are
  responsible for how you use this tool and for complying with the
  license terms of whatever model you run and the laws that apply to
  you. Don't use it to impersonate real people without consent, and
  keep any adult content to contexts involving only consenting adults.

## Architecture

```
chatai/
  app/
    main.py            FastAPI app + static file serving
    config.py           paths, host/port
    models.py            Pydantic schemas (Character, Persona, Chat, Settings)
    storage.py            JSON file persistence
    prompt.py              assembles system+persona+character+lorebook+history
    memory.py                LLM-driven history summarization
    lorebook.py                keyword-triggered world-info matching
    card_io.py                  SillyTavern v2 card import (.json/.png) + export
    providers/                   Ollama + OpenAI-compatible backends
    routers/                      characters / personas / chats / generate / settings
  web/                 no-build vanilla HTML/CSS/JS frontend
  characters/           example character card(s) you can import
  data/                (gitignored) your characters, personas, chats, settings
```

## Tests

```
cd chatai
pip install -r requirements.txt
python -m pytest tests/ -q
```
