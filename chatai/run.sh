#!/usr/bin/env bash
# Launches the private character-chat app, fully local.
# Usage: ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment (.venv)..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt

export CHATAI_HOST="${CHATAI_HOST:-127.0.0.1}"
export CHATAI_PORT="${CHATAI_PORT:-8765}"

echo ""
echo "Starting Private Character Chat at http://${CHATAI_HOST}:${CHATAI_PORT}"
echo "(binds to localhost only unless you set CHATAI_HOST=0.0.0.0 yourself)"
echo ""

exec python3 -m uvicorn app.main:app --host "$CHATAI_HOST" --port "$CHATAI_PORT"
