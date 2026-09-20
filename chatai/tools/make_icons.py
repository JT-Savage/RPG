#!/usr/bin/env python3
"""
Generate the PWA / home-screen icons in web/static/icons.

Pure standard library (zlib + struct): no Pillow, no build step, no network.
Re-run it after changing the palette or the glyph:

    python3 tools/make_icons.py

iOS needs real PNGs for `apple-touch-icon` (it ignores SVG), which is why
these are rasterized here and committed rather than drawn in the browser.
"""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "web" / "static" / "icons"

# Matches --accent / the gradient used for avatars in style.css.
VIOLET = (139, 92, 246)
INDIGO = (99, 102, 241)
INK = (26, 22, 43)

SAMPLES = 4  # per axis supersampling for anti-aliasing


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def gradient(u: float, v: float) -> tuple[int, int, int]:
    """Diagonal violet -> indigo, same direction as the CSS avatar gradient."""
    t = max(0.0, min(1.0, (u + v) / 2))
    return tuple(int(round(lerp(VIOLET[i], INDIGO[i], t))) for i in range(3))


def in_rounded_rect(u: float, v: float, cx: float, cy: float, hw: float, hh: float, r: float) -> bool:
    dx = abs(u - cx) - (hw - r)
    dy = abs(v - cy) - (hh - r)
    if dx <= 0 and dy <= 0:
        return True
    dx = max(dx, 0.0)
    dy = max(dy, 0.0)
    return (dx * dx + dy * dy) <= r * r


def in_circle(u: float, v: float, cx: float, cy: float, r: float) -> bool:
    return (u - cx) ** 2 + (v - cy) ** 2 <= r * r


def in_triangle(u: float, v: float, tri) -> bool:
    (ax, ay), (bx, by), (cx, cy) = tri

    def side(px, py, qx, qy):
        return (qx - px) * (v - py) - (qy - py) * (u - px)

    d1, d2, d3 = side(ax, ay, bx, by), side(bx, by, cx, cy), side(cx, cy, ax, ay)
    has_neg = d1 < 0 or d2 < 0 or d3 < 0
    has_pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (has_neg and has_pos)


def glyph_hit(u: float, v: float, scale: float):
    """Chat bubble + three dots, centred on (0.5, 0.5) and scaled about it.

    Returns None (background), "bubble" or "dot".
    """
    u = 0.5 + (u - 0.5) / scale
    v = 0.5 + (v - 0.5) / scale

    tail = ((0.355, 0.60), (0.55, 0.60), (0.345, 0.80))
    body = in_rounded_rect(u, v, 0.5, 0.455, 0.30, 0.225, 0.085)
    if not (body or in_triangle(u, v, tail)):
        return None
    for dx in (-0.125, 0.0, 0.125):
        if in_circle(u, v, 0.5 + dx, 0.455, 0.047):
            return "dot"
    return "bubble"


def render(size: int, *, corner: float, glyph_scale: float) -> bytes:
    """Render one icon and return its PNG bytes.

    corner: corner radius as a fraction of the size (0 = full-bleed square,
    which is what iOS home-screen icons and maskable icons want, since the
    platform applies its own mask).
    """
    step = 1.0 / (size * SAMPLES)
    rows = []
    for py in range(size):
        row = bytearray()
        for px in range(size):
            r_acc = g_acc = b_acc = a_acc = 0.0
            for sy in range(SAMPLES):
                v = (py * SAMPLES + sy + 0.5) * step
                for sx in range(SAMPLES):
                    u = (px * SAMPLES + sx + 0.5) * step
                    inside_bg = corner <= 0 or in_rounded_rect(u, v, 0.5, 0.5, 0.5, 0.5, corner)
                    if not inside_bg:
                        continue
                    hit = glyph_hit(u, v, glyph_scale)
                    if hit == "bubble":
                        col = (255, 255, 255)
                    elif hit == "dot":
                        col = INK
                    else:
                        col = gradient(u, v)
                    r_acc += col[0]
                    g_acc += col[1]
                    b_acc += col[2]
                    a_acc += 255
            n = SAMPLES * SAMPLES
            alpha = a_acc / n
            if alpha <= 0:
                row += bytes((0, 0, 0, 0))
            else:
                # Un-premultiply the covered samples so edges stay crisp.
                covered = a_acc / 255
                row += bytes((
                    int(round(r_acc / covered)),
                    int(round(g_acc / covered)),
                    int(round(b_acc / covered)),
                    int(round(alpha)),
                ))
        rows.append(bytes(row))

    raw = b"".join(b"\x00" + r for r in rows)
    return _png(size, raw)


def _chunk(tag: bytes, data: bytes) -> bytes:
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


def _png(size: int, raw: bytes) -> bytes:
    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)  # 8-bit RGBA
    return (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", header)
            + _chunk(b"IDAT", zlib.compress(raw, 9))
            + _chunk(b"IEND", b""))


TARGETS = [
    # name,                      size, corner, glyph scale
    ("icon-192.png",              192, 0.22, 1.00),
    ("icon-512.png",              512, 0.22, 1.00),
    # Maskable icons get cropped to a circle by some launchers: keep the
    # glyph inside the 80% safe zone and let the background run full bleed.
    ("maskable-512.png",          512, 0.00, 0.72),
    # iOS applies its own rounded mask, so no transparent corners here.
    ("apple-touch-icon-180.png",  180, 0.00, 0.86),
    ("favicon-32.png",             32, 0.22, 1.00),
]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, size, corner, scale in TARGETS:
        path = OUT_DIR / name
        path.write_bytes(render(size, corner=corner, glyph_scale=scale))
        print(f"wrote {path.relative_to(OUT_DIR.parent.parent.parent)} ({size}x{size})")


if __name__ == "__main__":
    main()
