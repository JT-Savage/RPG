#!/usr/bin/env bash
# Launches the private character-chat app.
#
# Usage:
#   ./run.sh                     localhost only (default, most private)
#   ./run.sh --lan               also reachable from your phone on the same Wi-Fi
#   ./run.sh --lan --https       same, over HTTPS (needed for full PWA/offline on iOS)
#   ./run.sh --lan --passcode hunter2
#
# Environment equivalents: CHATAI_HOST, CHATAI_PORT, CHATAI_PASSCODE.
set -euo pipefail
cd "$(dirname "$0")"

USE_HTTPS=0
LAN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --lan) LAN=1; shift ;;
    --https) USE_HTTPS=1; shift ;;
    --passcode) CHATAI_PASSCODE="${2:-}"; export CHATAI_PASSCODE; shift 2 ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment (.venv)..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt

if [ "$LAN" = "1" ]; then
  export CHATAI_HOST="0.0.0.0"
fi
export CHATAI_HOST="${CHATAI_HOST:-127.0.0.1}"
export CHATAI_PORT="${CHATAI_PORT:-8765}"

SSL_ARGS=()
SCHEME="http"
if [ "$USE_HTTPS" = "1" ]; then
  if python3 tools/make_cert.py; then
    SSL_ARGS=(--ssl-keyfile certs/dev-key.pem --ssl-certfile certs/dev-cert.pem)
    SCHEME="https"
  else
    echo "Continuing over plain http." >&2
  fi
fi

LAN_IP="$(python3 tools/netinfo.py 2>/dev/null || true)"

echo ""
echo "Private Character Chat"
echo "  on this machine:  ${SCHEME}://127.0.0.1:${CHATAI_PORT}"
if [ "$CHATAI_HOST" = "0.0.0.0" ] && [ -n "$LAN_IP" ]; then
  echo "  from your phone:  ${SCHEME}://${LAN_IP}:${CHATAI_PORT}"
  echo "                    (same Wi-Fi; in Safari use Share -> Add to Home Screen)"
fi
if [ "$CHATAI_HOST" != "127.0.0.1" ] && [ -z "${CHATAI_PASSCODE:-}" ]; then
  echo ""
  echo "  ! This is reachable by anything else on your network and has no"
  echo "    passcode set. Anyone on this Wi-Fi could read your chats."
  echo "    Re-run with:  ./run.sh --lan --passcode 'something-only-you-know'"
fi
if [ "$SCHEME" = "http" ] && [ "$CHATAI_HOST" != "127.0.0.1" ]; then
  echo ""
  echo "  Note: over plain http the app still installs to the home screen,"
  echo "        but iOS won't enable offline support. Add --https for that."
fi
echo ""

# ${SSL_ARGS[@]+...} keeps `set -u` happy with an empty array on bash 3.2 (macOS).
exec python3 -m uvicorn app.main:app --host "$CHATAI_HOST" --port "$CHATAI_PORT" ${SSL_ARGS[@]+"${SSL_ARGS[@]}"}
