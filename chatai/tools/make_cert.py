#!/usr/bin/env python3
"""
Create a self-signed certificate for serving the app over HTTPS on your LAN.

Why bother: iOS only registers a service worker (and only treats a page as
a proper installable app with offline support) on a secure context. Plain
http://192.168.x.x is not one. localhost is, so this is only needed for
reaching the app from a phone.

The certificate is self-signed, so Safari will warn the first time —
that's expected; see the README for trusting it on iOS. Keys never leave
this machine and certs/ is gitignored.

    python3 tools/make_cert.py [--force]
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from netinfo import lan_ip  # noqa: E402

CERT_DIR = Path(__file__).resolve().parent.parent / "certs"
CERT_FILE = CERT_DIR / "dev-cert.pem"
KEY_FILE = CERT_DIR / "dev-key.pem"

CONFIG_TEMPLATE = """\
[req]
distinguished_name = dn
x509_extensions = v3
prompt = no

[dn]
CN = Private Character Chat

[v3]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt

[alt]
DNS.1 = localhost
IP.1 = 127.0.0.1
IP.2 = ::1
{extra}
"""


def have_openssl() -> bool:
    try:
        subprocess.run(["openssl", "version"], check=True, capture_output=True)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def cert_covers(ip: str) -> bool:
    if not (CERT_FILE.exists() and KEY_FILE.exists()):
        return False
    if not ip:
        return True
    try:
        out = subprocess.run(["openssl", "x509", "-in", str(CERT_FILE), "-noout", "-text"],
                             check=True, capture_output=True, text=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return False
    return f"IP Address:{ip}" in out


def generate(ip: str) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    extra = f"IP.3 = {ip}\n" if ip else ""
    with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as fh:
        fh.write(CONFIG_TEMPLATE.format(extra=extra))
        cnf = fh.name
    try:
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-sha256",
            "-days", "3650", "-nodes",
            "-keyout", str(KEY_FILE), "-out", str(CERT_FILE),
            "-config", cnf,
        ], check=True, capture_output=True)
    finally:
        Path(cnf).unlink(missing_ok=True)
    try:
        KEY_FILE.chmod(0o600)
    except OSError:
        pass


def main() -> int:
    force = "--force" in sys.argv
    ip = lan_ip()

    if not force and cert_covers(ip):
        print(f"Reusing existing certificate: {CERT_FILE}")
        return 0

    if not have_openssl():
        print("openssl not found — cannot create an HTTPS certificate.\n"
              "Install OpenSSL, or run over plain http:// (the app still works,\n"
              "just without offline support on the phone).", file=sys.stderr)
        return 1

    generate(ip)
    print(f"Created self-signed certificate for {ip or 'localhost'}: {CERT_FILE}")
    print("Safari will warn the first time you open it — see the README.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
