#!/usr/bin/env python3
"""
Map Background Generator for "There Will Be Kobolds"
Generates one pre-composed 512x448 background PNG per location
(2x2 screens of the 256x224 SNES-style viewport), rendered in a
16x16 tile-grid style with biome-specific palettes and props.

Run: python3 generate_maps.py (any cwd; output paths are absolute-safe
when run from godot_project/assets/, files land in assets/maps/).

Uses only stdlib (struct, zlib, random) - no Pillow/numpy.
PNG writer helpers copied from generate_assets.py.
"""
import struct
import zlib
import os
import random

# ===== PNG WRITER (copied from generate_assets.py, no external deps) =====

def _make_png(width: int, height: int, pixels: list) -> bytes:
    """pixels = list of (R,G,B,A) tuples, row-major"""
    def chunk(name: bytes, data: bytes) -> bytes:
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = chunk(b'IHDR', ihdr_data)

    raw_rows = []
    for y in range(height):
        row = bytearray(b'\x00')  # Filter type None
        base = y * width
        for x in range(width):
            r, g, b, a = pixels[base + x]
            row += bytes((r, g, b, a))
        raw_rows.append(bytes(row))

    compressed = zlib.compress(b''.join(raw_rows), 9)
    idat = chunk(b'IDAT', compressed)
    iend = chunk(b'IEND', b'')

    return sig + ihdr + idat + iend

def save_png(path: str, width: int, height: int, pixels: list) -> None:
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'wb') as f:
        f.write(_make_png(width, height, pixels))
    size = os.path.getsize(path)
    print(f"  + {path} ({width}x{height}, {size} bytes)")

# ===== MAP CANVAS =====

MAP_W = 512   # 2 screens wide  (viewport 256)
MAP_H = 448   # 2 screens tall  (viewport 224)
TILE = 16
WALL = 16     # border wall thickness in pixels


class MapCanvas:
    """Simple RGBA pixel canvas with tile-style drawing helpers."""

    def __init__(self, w: int = MAP_W, h: int = MAP_H, seed: int = 0):
        self.w = w
        self.h = h
        self.px = [(0, 0, 0, 255)] * (w * h)
        self.rng = random.Random(seed)

    # -- primitives ------------------------------------------------------

    def set(self, x: int, y: int, c: tuple):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y * self.w + x] = c

    def get(self, x: int, y: int) -> tuple:
        return self.px[y * self.w + x]

    def draw_rect(self, x: int, y: int, w: int, h: int, c: tuple):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            row = yy * self.w
            for xx in range(x0, x1):
                self.px[row + xx] = c

    def draw_circle(self, cx: int, cy: int, r: int, c: tuple):
        r2 = r * r
        for yy in range(max(0, cy - r), min(self.h, cy + r + 1)):
            for xx in range(max(0, cx - r), min(self.w, cx + r + 1)):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r2:
                    self.px[yy * self.w + xx] = c

    # -- floor -----------------------------------------------------------

    def draw_tile_floor(self, shades: list, dither: tuple = None):
        """Fill whole canvas with 16px tiles in alternating shades.
        shades: list of 2-3 RGBA colors. dither: optional accent color used
        as a subtle 2px checker inside each tile."""
        for ty in range(0, self.h, TILE):
            for tx in range(0, self.w, TILE):
                shade = shades[self.rng.randrange(len(shades))]
                for yy in range(ty, min(ty + TILE, self.h)):
                    row = yy * self.w
                    for xx in range(tx, min(tx + TILE, self.w)):
                        c = shade
                        if dither and ((xx // 2) + (yy // 2)) % 2 == 0:
                            # subtle blend toward dither color
                            c = tuple((c[i] * 3 + dither[i]) // 4 for i in range(3)) + (255,)
                        self.px[row + xx] = c
                # faint tile seam (bottom-right edge) for grid readability
                seam = tuple(max(0, v - 8) for v in shade[:3]) + (255,)
                for xx in range(tx, min(tx + TILE, self.w)):
                    self.set(xx, min(ty + TILE - 1, self.h - 1), seam)
                for yy in range(ty, min(ty + TILE, self.h)):
                    self.set(min(tx + TILE - 1, self.w - 1), yy, seam)

    # -- border wall -----------------------------------------------------

    def draw_border_walls(self, wall: tuple, highlight: tuple, shadow: tuple = None):
        """16px thick walls around all edges, darker shade with a simple
        3D highlight strip on the inner edge."""
        if shadow is None:
            shadow = tuple(max(0, v - 25) for v in wall[:3]) + (255,)
        # solid wall band
        self.draw_rect(0, 0, self.w, WALL, wall)               # top
        self.draw_rect(0, self.h - WALL, self.w, WALL, wall)   # bottom
        self.draw_rect(0, 0, WALL, self.h, wall)               # left
        self.draw_rect(self.w - WALL, 0, WALL, self.h, wall)   # right
        # brick-ish vertical seams on the wall band
        for tx in range(0, self.w, TILE):
            for yy in range(0, WALL):
                self.set(tx, yy, shadow)
                self.set(tx, self.h - WALL + yy, shadow)
        for ty in range(0, self.h, TILE):
            for xx in range(0, WALL):
                self.set(xx, ty, shadow)
                self.set(self.w - WALL + xx, ty, shadow)
        # 3D highlight: bright strip on the inner edge of top/left walls,
        # shadow strip on inner edge of bottom/right walls
        self.draw_rect(WALL - 2, WALL - 2, self.w - 2 * WALL + 4, 2, highlight)
        self.draw_rect(WALL - 2, WALL - 2, 2, self.h - 2 * WALL + 4, highlight)
        self.draw_rect(WALL - 2, self.h - WALL, self.w - 2 * WALL + 4, 2, shadow)
        self.draw_rect(self.w - WALL, WALL - 2, 2, self.h - 2 * WALL + 4, shadow)

    # -- prop scattering ---------------------------------------------------

    def scatter_props(self, count: int, draw_fn, margin: int = 28):
        """Call draw_fn(canvas, x, y, rng) at `count` seeded-random spots
        inside the walls."""
        for _ in range(count):
            x = self.rng.randrange(margin, self.w - margin)
            y = self.rng.randrange(margin, self.h - margin)
            draw_fn(self, x, y, self.rng)


# ===== PROP DRAWERS (each: fn(canvas, x, y, rng)) =====

def prop_pebble(c, x, y, rng):
    shade = rng.choice([(110, 95, 80, 255), (95, 82, 70, 255), (125, 108, 90, 255)])
    c.draw_circle(x, y, rng.randrange(1, 3), shade)

def prop_bone(c, x, y, rng):
    bone = (215, 200, 170, 255)
    if rng.random() < 0.5:
        for i in range(5):
            c.set(x + i, y, bone)
        c.set(x - 1, y - 1, bone); c.set(x - 1, y + 1, bone)
        c.set(x + 5, y - 1, bone); c.set(x + 5, y + 1, bone)
    else:  # small skull
        c.draw_rect(x, y, 4, 3, bone)
        c.set(x + 1, y + 1, (60, 50, 45, 255))
        c.set(x + 3, y + 1, (60, 50, 45, 255))

def prop_tree(c, x, y, rng):
    trunk = (90, 60, 35, 255)
    canopy = (35, 95, 30, 255)
    canopy_hi = (50, 120, 40, 255)
    c.draw_rect(x - 2, y, 4, 10, trunk)
    c.draw_circle(x, y - 6, 9, canopy)
    c.draw_circle(x - 3, y - 9, 5, canopy_hi)

def prop_bush(c, x, y, rng):
    c.draw_circle(x, y, 5, (45, 110, 35, 255))
    c.draw_circle(x - 2, y - 2, 3, (65, 135, 45, 255))

def prop_hut(c, x, y, rng):
    wall = (130, 90, 50, 255)
    wall_dk = (105, 72, 40, 255)
    roof = (90, 60, 30, 255)
    roof_hi = (115, 80, 42, 255)
    w, h = 28, 20
    c.draw_rect(x, y, w, h, wall)
    c.draw_rect(x, y + h - 3, w, 3, wall_dk)
    # door
    c.draw_rect(x + w // 2 - 3, y + h - 9, 6, 9, (70, 48, 28, 255))
    # triangular thatch roof
    for i in range(10):
        c.draw_rect(x - 2 + i * (w + 4) // 20, y - 10 + i, (w + 4) - 2 * (i * (w + 4) // 20), 1,
                    roof_hi if i < 3 else roof)

def prop_facade(c, x, y, rng):
    stone = (150, 145, 140, 255)
    stone_dk = (120, 115, 112, 255)
    roof = (105, 70, 60, 255)
    w, h = 34, 24
    c.draw_rect(x, y, w, h, stone)
    for ry in range(y, y + h, 4):
        for rx in range(x, x + w, 8):
            c.set(rx + (ry // 4 % 2) * 4, ry, stone_dk)
    c.draw_rect(x - 2, y - 6, w + 4, 6, roof)
    # windows + door
    c.draw_rect(x + 4, y + 5, 5, 5, (70, 90, 130, 255))
    c.draw_rect(x + w - 9, y + 5, 5, 5, (70, 90, 130, 255))
    c.draw_rect(x + w // 2 - 3, y + h - 10, 7, 10, (85, 60, 40, 255))

def prop_tomb(c, x, y, rng):
    slab = (75, 78, 95, 255)
    slab_hi = (95, 98, 118, 255)
    c.draw_rect(x, y, 14, 9, slab)
    c.draw_rect(x, y, 14, 2, slab_hi)
    c.draw_rect(x + 5, y - 5, 4, 5, slab)   # headstone
    c.set(x + 6, y - 3, (50, 52, 65, 255))

def prop_candle(c, x, y, rng):
    c.draw_rect(x, y, 2, 4, (220, 210, 180, 255))
    c.set(x, y - 1, (255, 200, 80, 255))
    c.set(x + 1, y - 1, (255, 160, 40, 255))
    # glow
    for dx, dy in ((-1, -1), (2, -1), (0, -2), (1, -2)):
        gx, gy = x + dx, y + dy
        if 0 <= gx < c.w and 0 <= gy < c.h:
            r, g, b, _ = c.get(gx, gy)
            c.set(gx, gy, (min(255, r + 50), min(255, g + 35), b, 255))

def prop_water_patch(c, x, y, rng):
    murk = (45, 70, 55, 255)
    murk_dk = (35, 58, 48, 255)
    r = rng.randrange(8, 16)
    c.draw_circle(x, y, r, murk)
    c.draw_circle(x + r // 3, y + r // 3, max(2, r - 5), murk_dk)
    # ripple highlight
    for i in range(-r // 2, r // 2):
        c.set(x + i, y - r // 3, (70, 100, 80, 255))

def prop_reed(c, x, y, rng):
    stalk = (85, 110, 50, 255)
    for i in range(3):
        h = rng.randrange(5, 9)
        for j in range(h):
            c.set(x + i * 2, y - j, stalk)
        c.set(x + i * 2, y - h, (130, 120, 70, 255))

def prop_snow_patch(c, x, y, rng):
    snow = (235, 240, 245, 255)
    snow_dim = (210, 218, 228, 255)
    r = rng.randrange(6, 13)
    c.draw_circle(x, y, r, snow_dim)
    c.draw_circle(x - 1, y - 1, max(2, r - 3), snow)

def prop_boulder(c, x, y, rng):
    rock = (120, 122, 128, 255)
    rock_hi = (150, 152, 158, 255)
    rock_dk = (92, 94, 100, 255)
    r = rng.randrange(4, 8)
    c.draw_circle(x, y, r, rock)
    c.draw_circle(x - r // 3, y - r // 3, max(1, r // 2), rock_hi)
    c.draw_circle(x + r // 3, y + r // 2, max(1, r // 3), rock_dk)

def prop_tent(c, x, y, rng):
    cloth = (150, 120, 70, 255) if rng.random() < 0.6 else (130, 70, 60, 255)
    cloth_dk = tuple(max(0, v - 30) for v in cloth[:3]) + (255,)
    w, h = 26, 16
    # triangle tent
    for i in range(h):
        half = (i * w) // (2 * h)
        c.draw_rect(x - half, y - h + i, half * 2 + 1, 1, cloth if i % 4 else cloth_dk)
    # entrance flap
    c.draw_rect(x - 2, y - 6, 4, 6, (60, 45, 30, 255))

def prop_campfire(c, x, y, rng):
    c.draw_circle(x, y, 4, (80, 65, 55, 255))      # stone ring
    c.draw_circle(x, y, 2, (220, 110, 30, 255))    # fire
    c.set(x, y - 2, (250, 190, 70, 255))
    c.set(x - 1, y - 1, (240, 150, 40, 255))
    # log
    c.draw_rect(x - 5, y + 3, 10, 2, (100, 70, 40, 255))

def prop_cactus(c, x, y, rng):
    green = (60, 130, 60, 255)
    green_hi = (85, 155, 80, 255)
    h = rng.randrange(8, 14)
    c.draw_rect(x, y - h, 3, h, green)
    c.draw_rect(x, y - h, 1, h, green_hi)
    if h > 9:
        c.draw_rect(x - 4, y - h + 3, 4, 2, green)
        c.draw_rect(x - 4, y - h + 1, 2, 4, green)
        c.draw_rect(x + 3, y - h + 5, 4, 2, green)
        c.draw_rect(x + 5, y - h + 3, 2, 4, green)

def prop_crystal(c, x, y, rng):
    body = (150, 200, 230, 255)
    glow = (200, 235, 255, 255)
    h = rng.randrange(6, 11)
    for i in range(h):
        half = max(0, (h - i) // 3)
        c.draw_rect(x - half, y - i, half * 2 + 1, 1, body)
    c.set(x, y - h + 1, glow)
    c.set(x - 1, y - h // 2, glow)

def prop_flower(c, x, y, rng):
    petal = rng.choice([(230, 110, 140, 255), (240, 200, 90, 255), (200, 130, 220, 255)])
    c.set(x, y, (250, 240, 200, 255))
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        c.set(x + dx, y + dy, petal)
    c.set(x, y + 2, (50, 120, 45, 255))

def prop_rune(c, x, y, rng):
    glow = (170, 70, 230, 255)
    dim = (110, 45, 160, 255)
    pts = [(0, 0), (1, 1), (2, 0), (1, 2), (0, 3), (2, 3), (1, 4)]
    rng.shuffle(pts)
    for px, py in pts[:5]:
        c.set(x + px, y + py, glow)
    for px, py in pts[5:]:
        c.set(x + px, y + py, dim)
    # faint glow halo
    for dx in range(-2, 5):
        for dy in range(-2, 7):
            gx, gy = x + dx, y + dy
            if 0 <= gx < c.w and 0 <= gy < c.h:
                r, g, b, _ = c.get(gx, gy)
                if (r, g, b) not in ((170, 70, 230), (110, 45, 160)):
                    c.set(gx, gy, (min(255, r + 12), g, min(255, b + 20), 255))

def prop_cage(c, x, y, rng):
    bar = (90, 80, 70, 255)
    bar_hi = (120, 108, 95, 255)
    w, h = 14, 12
    c.draw_rect(x, y, w, 2, bar_hi)            # top
    c.draw_rect(x, y + h - 2, w, 2, bar)       # bottom
    for bx in range(x, x + w, 3):
        c.draw_rect(bx, y, 1, h, bar)
    # shadow inside
    c.draw_rect(x + 1, y + h - 4, w - 2, 2, (55, 48, 42, 255))

def prop_wood_structure(c, x, y, rng):
    plank = (140, 100, 60, 255)
    plank_dk = (115, 82, 48, 255)
    w, h = rng.randrange(16, 26), rng.randrange(10, 16)
    c.draw_rect(x, y, w, h, plank)
    for py in range(y, y + h, 3):
        c.draw_rect(x, py, w, 1, plank_dk)
    c.draw_rect(x, y, 2, h, plank_dk)

def prop_dune(c, x, y, rng):
    """Wavy lighter band across part of the map."""
    light = (235, 210, 150, 255)
    w = rng.randrange(60, 140)
    for i in range(w):
        yy = y + int(3 * __import__('math').sin(i / 9.0))
        c.set(x + i, yy, light)
        c.set(x + i, yy + 1, light)

def prop_grass_tuft(c, x, y, rng):
    g = rng.choice([(70, 150, 50, 255), (85, 165, 60, 255)])
    c.set(x, y, g); c.set(x + 2, y, g); c.set(x + 1, y - 1, g)

def prop_sand_edge_shell(c, x, y, rng):
    c.draw_circle(x, y, 2, (240, 225, 200, 255))
    c.set(x, y, (210, 180, 160, 255))

def prop_fungus(c, x, y, rng):
    cap = (160, 80, 170, 255)
    c.draw_rect(x, y, 2, 3, (200, 190, 170, 255))
    c.draw_rect(x - 1, y - 2, 4, 2, cap)


# ===== BIOME MAP BUILDERS =====

def stable_seed(name: str) -> int:
    return zlib.crc32(name.encode('utf-8')) & 0x7FFFFFFF


def build_map(loc_id: str) -> MapCanvas:
    c = MapCanvas(MAP_W, MAP_H, seed=stable_seed(loc_id))
    r = c.rng

    if loc_id == "tutorial_warren":
        c.draw_tile_floor([(120, 88, 56, 255), (108, 78, 50, 255), (130, 96, 62, 255)],
                          dither=(96, 70, 46, 255))
        c.draw_border_walls((78, 66, 60, 255), (108, 94, 84, 255))
        c.scatter_props(70, prop_pebble)
        c.scatter_props(14, prop_bone)
        c.scatter_props(8, prop_fungus)

    elif loc_id == "surface_forest":
        c.draw_tile_floor([(72, 142, 52, 255), (62, 128, 44, 255), (82, 154, 60, 255)],
                          dither=(56, 116, 40, 255))
        c.draw_border_walls((40, 88, 32, 255), (58, 112, 44, 255))
        c.scatter_props(60, prop_grass_tuft)
        c.scatter_props(16, prop_bush)
        c.scatter_props(18, prop_tree)

    elif loc_id == "kobold_village":
        c.draw_tile_floor([(150, 112, 68, 255), (76, 140, 52, 255), (140, 102, 60, 255)],
                          dither=(120, 92, 56, 255))
        c.draw_border_walls((96, 72, 48, 255), (124, 96, 64, 255))
        # central dirt plaza
        c.draw_rect(176, 144, 160, 160, (158, 120, 74, 255))
        c.scatter_props(40, prop_grass_tuft)
        c.scatter_props(30, prop_pebble)
        c.scatter_props(7, prop_hut)

    elif loc_id == "imperial_city":
        c.draw_tile_floor([(150, 148, 145, 255), (134, 132, 130, 255), (162, 160, 156, 255)],
                          dither=(122, 120, 118, 255))
        c.draw_border_walls((100, 98, 96, 255), (134, 132, 128, 255))
        # fountain square in the centre
        cx, cy = MAP_W // 2, MAP_H // 2
        c.draw_circle(cx, cy, 26, (120, 118, 116, 255))   # plaza rim
        c.draw_circle(cx, cy, 20, (70, 110, 170, 255))    # water
        c.draw_circle(cx, cy, 6, (160, 158, 154, 255))    # pedestal
        c.draw_circle(cx, cy - 2, 2, (200, 220, 245, 255))  # spout
        c.scatter_props(8, prop_facade)
        c.scatter_props(24, prop_pebble)

    elif loc_id in ("catacomb_entrance", "catacomb_depths"):
        dark = loc_id == "catacomb_depths"
        base = [(70, 72, 92, 255), (60, 62, 80, 255), (80, 82, 102, 255)] if not dark else \
               [(56, 58, 78, 255), (48, 50, 66, 255), (64, 66, 86, 255)]
        c.draw_tile_floor(base, dither=(44, 46, 60, 255))
        c.draw_border_walls((40, 42, 58, 255), (66, 68, 88, 255))
        c.scatter_props(12 if not dark else 16, prop_tomb)
        c.scatter_props(14, prop_candle)
        c.scatter_props(20, prop_pebble)
        if dark:
            c.scatter_props(8, prop_bone)

    elif loc_id == "swamp_village":
        c.draw_tile_floor([(86, 104, 60, 255), (74, 92, 54, 255), (96, 108, 64, 255)],
                          dither=(66, 84, 50, 255))
        c.draw_border_walls((54, 70, 44, 255), (76, 94, 58, 255))
        c.scatter_props(12, prop_water_patch)
        c.scatter_props(26, prop_reed)
        c.scatter_props(5, prop_hut)

    elif loc_id == "mountain_pass":
        c.draw_tile_floor([(138, 140, 146, 255), (124, 126, 132, 255), (150, 152, 158, 255)],
                          dither=(112, 114, 120, 255))
        c.draw_border_walls((88, 90, 98, 255), (118, 120, 128, 255))
        c.scatter_props(16, prop_snow_patch)
        c.scatter_props(18, prop_boulder)
        c.scatter_props(24, prop_pebble)

    elif loc_id == "army_camp":
        c.draw_tile_floor([(146, 110, 68, 255), (134, 100, 62, 255), (156, 120, 74, 255)],
                          dither=(118, 90, 56, 255))
        c.draw_border_walls((94, 72, 48, 255), (122, 96, 64, 255))
        c.scatter_props(9, prop_tent)
        c.scatter_props(5, prop_campfire)
        c.scatter_props(30, prop_pebble)
        c.scatter_props(16, prop_grass_tuft)

    elif loc_id == "desert_region":
        c.draw_tile_floor([(222, 192, 124, 255), (208, 178, 110, 255), (232, 204, 138, 255)],
                          dither=(196, 168, 102, 255))
        c.draw_border_walls((172, 142, 86, 255), (204, 176, 112, 255))
        c.scatter_props(14, prop_dune)
        c.scatter_props(12, prop_cactus)
        c.scatter_props(20, prop_pebble)

    elif loc_id == "floating_island":
        c.draw_tile_floor([(150, 190, 140, 255), (136, 176, 128, 255), (164, 202, 152, 255)],
                          dither=(126, 164, 120, 255))
        # purple sky-void border instead of normal wall colors
        c.draw_border_walls((86, 60, 130, 255), (130, 100, 180, 255), (60, 40, 95, 255))
        # extra void fade just inside the wall
        for i in range(6):
            t = i / 6.0
            fade = (int(86 + (150 - 86) * t), int(60 + (190 - 60) * t),
                    int(130 + (140 - 130) * t), 255)
            c.draw_rect(WALL + i, WALL + i, MAP_W - 2 * (WALL + i), 1, fade)
            c.draw_rect(WALL + i, MAP_H - WALL - 1 - i, MAP_W - 2 * (WALL + i), 1, fade)
            c.draw_rect(WALL + i, WALL + i, 1, MAP_H - 2 * (WALL + i), fade)
            c.draw_rect(MAP_W - WALL - 1 - i, WALL + i, 1, MAP_H - 2 * (WALL + i), fade)
        c.scatter_props(14, prop_crystal)
        c.scatter_props(30, prop_grass_tuft)

    elif loc_id == "orisia_island":
        c.draw_tile_floor([(66, 158, 70, 255), (56, 144, 60, 255), (78, 170, 82, 255)],
                          dither=(50, 132, 54, 255))
        c.draw_border_walls((196, 172, 116, 255), (222, 198, 140, 255), (168, 146, 96, 255))
        # sandy edge band inside the border
        c.draw_rect(WALL, WALL, MAP_W - 2 * WALL, 10, (214, 190, 132, 255))
        c.draw_rect(WALL, MAP_H - WALL - 10, MAP_W - 2 * WALL, 10, (214, 190, 132, 255))
        c.draw_rect(WALL, WALL, 10, MAP_H - 2 * WALL, (214, 190, 132, 255))
        c.draw_rect(MAP_W - WALL - 10, WALL, 10, MAP_H - 2 * WALL, (214, 190, 132, 255))
        c.scatter_props(30, prop_flower)
        c.scatter_props(24, prop_grass_tuft)
        c.scatter_props(10, prop_bush)
        c.scatter_props(8, prop_tree)

    elif loc_id == "final_dungeon":
        c.draw_tile_floor([(38, 26, 52, 255), (30, 20, 42, 255), (46, 32, 62, 255)],
                          dither=(24, 16, 34, 255))
        c.draw_border_walls((22, 14, 32, 255), (70, 44, 100, 255), (10, 6, 16, 255))
        c.scatter_props(22, prop_rune)
        c.scatter_props(10, prop_candle)

    elif loc_id == "slaver_island":
        c.draw_tile_floor([(218, 190, 130, 255), (204, 176, 118, 255), (228, 200, 142, 255)],
                          dither=(190, 164, 108, 255))
        c.draw_border_walls((150, 116, 72, 255), (182, 146, 96, 255))
        c.scatter_props(6, prop_wood_structure)
        c.scatter_props(7, prop_cage)
        c.scatter_props(12, prop_sand_edge_shell)
        c.scatter_props(16, prop_pebble)

    else:
        raise ValueError(f"Unknown location id: {loc_id}")

    return c


# ===== MAIN =====

LOCATION_IDS = [
    "tutorial_warren", "surface_forest", "kobold_village", "imperial_city",
    "catacomb_entrance", "catacomb_depths", "swamp_village", "mountain_pass",
    "army_camp", "desert_region", "floating_island", "orisia_island",
    "final_dungeon", "slaver_island",
]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
    print(f"Generating {len(LOCATION_IDS)} map backgrounds ({MAP_W}x{MAP_H}) -> {out_dir}")
    print("=" * 60)
    for loc_id in LOCATION_IDS:
        canvas = build_map(loc_id)
        save_png(os.path.join(out_dir, f"{loc_id}.png"), canvas.w, canvas.h, canvas.px)
    print("=" * 60)
    print("Map generation complete. Import with Texture Filter = Nearest.")


if __name__ == "__main__":
    main()
