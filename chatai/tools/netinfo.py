#!/usr/bin/env python3
"""Print this machine's LAN IPv4 address (the one a phone would use).

No network traffic is sent: opening a UDP socket toward a public address
only makes the OS pick the interface it *would* route through.
"""
from __future__ import annotations

import socket
import sys


def lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return ""
    finally:
        s.close()


if __name__ == "__main__":
    ip = lan_ip()
    if not ip or ip.startswith("127."):
        sys.exit(1)
    print(ip)
