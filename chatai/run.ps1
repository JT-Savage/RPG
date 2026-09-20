# Launches the private character-chat app on Windows.
#
#   .\run.ps1                          localhost only (default, most private)
#   .\run.ps1 -Lan                     also reachable from your phone on the same Wi-Fi
#   .\run.ps1 -Lan -Https              same, over HTTPS (needed for full PWA/offline on iOS)
#   .\run.ps1 -Lan -Passcode hunter2
param(
    [switch]$Lan,
    [switch]$Https,
    [string]$Passcode
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment (.venv)..."
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
pip install -q -r requirements.txt

if ($Lan) { $env:CHATAI_HOST = "0.0.0.0" }
if (-not $env:CHATAI_HOST) { $env:CHATAI_HOST = "127.0.0.1" }
if (-not $env:CHATAI_PORT) { $env:CHATAI_PORT = "8765" }
if ($Passcode) { $env:CHATAI_PASSCODE = $Passcode }

$sslArgs = @()
$scheme = "http"
if ($Https) {
    python tools\make_cert.py
    if ($LASTEXITCODE -eq 0) {
        $sslArgs = @("--ssl-keyfile", "certs\dev-key.pem", "--ssl-certfile", "certs\dev-cert.pem")
        $scheme = "https"
    } else {
        Write-Warning "Could not create a certificate (is OpenSSL installed?). Continuing over plain http."
    }
}

$lanIp = ""
try { $lanIp = (python tools\netinfo.py) } catch { $lanIp = "" }

Write-Host ""
Write-Host "Private Character Chat"
Write-Host "  on this machine:  ${scheme}://127.0.0.1:$($env:CHATAI_PORT)"
if ($env:CHATAI_HOST -eq "0.0.0.0" -and $lanIp) {
    Write-Host "  from your phone:  ${scheme}://${lanIp}:$($env:CHATAI_PORT)"
    Write-Host "                    (same Wi-Fi; in Safari use Share -> Add to Home Screen)"
}
if ($env:CHATAI_HOST -ne "127.0.0.1" -and -not $env:CHATAI_PASSCODE) {
    Write-Host ""
    Write-Warning "Reachable by anything else on your network with no passcode set."
    Write-Host "    Re-run with:  .\run.ps1 -Lan -Passcode 'something-only-you-know'"
}
if ($scheme -eq "http" -and $env:CHATAI_HOST -ne "127.0.0.1") {
    Write-Host ""
    Write-Host "  Note: over plain http the app still installs to the home screen,"
    Write-Host "        but iOS won't enable offline support. Add -Https for that."
}
Write-Host ""

python -m uvicorn app.main:app --host $env:CHATAI_HOST --port $env:CHATAI_PORT @sslArgs
