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

It is also an installable PWA, so you can add it to an iPhone (or
Android) home screen and use it full-screen, like an app — it still
talks only to the machine on your own Wi-Fi that's running it. See
[Using it from your phone](#using-it-from-your-phone).

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
- Installable on a phone: home-screen icon, full-screen (no Safari
  chrome), a slide-out menu, safe-area handling for the notch and home
  indicator, and an offline shell so launching it while your machine is
  asleep gives you a clear message instead of a browser error page.
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

Options (all optional):

| Flag | Effect |
| --- | --- |
| `--lan` / `-Lan` | also listen on your LAN, so a phone can reach it |
| `--https` / `-Https` | serve over HTTPS with a self-signed cert |
| `--passcode X` / `-Passcode X` | require a passcode before anything loads |

See [Using it from your phone](#using-it-from-your-phone).

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

## Using it from your phone

The server runs on your computer; your phone is just the screen. Both
have to be on the same Wi-Fi, and the computer has to be awake with
`run.sh` still going.

### 1. Start it so the phone can reach it

```
./run.sh --lan --passcode 'something-only-you-know'     # macOS/Linux
.\run.ps1 -Lan -Passcode 'something-only-you-know'      # Windows
```

`--lan` binds to `0.0.0.0` instead of loopback, and the script prints
the exact URL to type on the phone, e.g. `http://192.168.1.42:8765`.

**Set a passcode whenever you use `--lan`.** Without one, anything else
on that network — a guest's laptop, a smart TV — can open your chats by
guessing the address. With one, each device asks for it once and then
stays signed in. The app warns you at startup if you skip it. (You can
also set `CHATAI_PASSCODE` in the environment instead of passing it on
the command line, which keeps it out of your shell history.)

If your computer's firewall prompts you to allow incoming connections
for Python, say yes — that's the phone reaching the server.

### 2. Add it to the home screen

On iPhone, open the URL in **Safari** (not Chrome — only Safari can
install web apps on iOS), tap the **Share** button, then **Add to Home
Screen**. The app then launches full-screen with its own icon, no
address bar.

On Android/Chrome you'll get an **Install** button in the app itself.

### 3. Optional: HTTPS, for offline support

iOS only enables service workers — the bit that caches the app shell so
it opens instantly and can show a proper "can't reach your server"
screen — on a secure origin. `http://192.168.x.x` isn't one. Everything
except that caching works fine over plain http, so this step is
optional.

To get it:

```
./run.sh --lan --https --passcode '…'
```

That generates a self-signed certificate under `chatai/certs/`
(gitignored, never leaves your machine) covering `localhost` and your
current LAN IP, and serves over `https://`. Safari will warn that the
certificate isn't trusted the first time; you can tap through the
warning, or trust it properly on the phone:

1. Email/AirDrop `chatai/certs/dev-cert.pem` to the phone and open it.
2. **Settings → General → VPN & Device Management** → install the
   profile.
3. **Settings → General → About → Certificate Trust Settings** → switch
   it on.

Note the certificate is pinned to the LAN IP it was made for; if your
router hands the computer a different address later, re-run with
`python3 tools/make_cert.py --force`.

### Notes

- Your chat history lives on the computer, not the phone, so switching
  between desktop and phone picks up exactly where you left off.
- The app reopens your last chat on launch.
- Swipe in from the left edge (or tap ☰) for the chat/character list.
- Generation speed is whatever your computer's model server manages —
  the phone does no inference at all, and its battery barely notices.

## Notes on privacy & responsible use

- This app does not phone home, does not use analytics, and has no
  account system. Your chats live only in `chatai/data/` on this
  machine.
- Running with `--lan` makes it reachable by every device on your
  network, which is the point when you want it on a phone — but set a
  passcode, and don't port-forward it to the open internet. The
  passcode is one shared secret with a simple brute-force brake, not a
  hardened authentication system.
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
    auth.py                       optional shared-passcode gate for LAN use
    routers/                      characters / personas / chats / generate / settings
  web/                 no-build vanilla HTML/CSS/JS frontend
    manifest.webmanifest  PWA manifest (icons, name, standalone display)
    sw.js                  service worker: caches the shell, never the API
    offline.html            shown when the server can't be reached
  tools/               icon generator, LAN IP lookup, self-signed cert helper
  characters/           example character card(s) you can import
  data/                (gitignored) your characters, personas, chats, settings
```

## Tests

```
cd chatai
pip install -r requirements.txt
python -m pytest tests/ -q
```
