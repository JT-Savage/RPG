# Launches the private character-chat app, fully local, on Windows.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment (.venv)..."
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
pip install -q -r requirements.txt

if (-not $env:CHATAI_HOST) { $env:CHATAI_HOST = "127.0.0.1" }
if (-not $env:CHATAI_PORT) { $env:CHATAI_PORT = "8765" }

Write-Host ""
Write-Host "Starting Private Character Chat at http://$($env:CHATAI_HOST):$($env:CHATAI_PORT)"
Write-Host "(binds to localhost only unless you set CHATAI_HOST=0.0.0.0 yourself)"
Write-Host ""

python -m uvicorn app.main:app --host $env:CHATAI_HOST --port $env:CHATAI_PORT
