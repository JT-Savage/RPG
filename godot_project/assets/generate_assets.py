#!/usr/bin/env python3
"""
Pixel Art Asset Generator for "There Will Be Kobolds"
Generates all placeholder PNG assets in proper 16-bit SNES style.
Run: python3 generate_assets.py (from godot_project/assets/ directory)

Uses only stdlib (struct, zlib) to write PNG files without Pillow dependency.
"""
import struct
import zlib
import os
import math

# ===== PNG WRITER (no external deps) =====

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
        row = b'\x00'  # Filter type None
        for x in range(width):
            r, g, b, a = pixels[y * width + x]
            row += bytes([r, g, b, a])
        raw_rows.append(row)

    compressed = zlib.compress(b''.join(raw_rows), 9)
    idat = chunk(b'IDAT', compressed)
    iend = chunk(b'IEND', b'')

    return sig + ihdr + idat + iend

def save_png(path: str, width: int, height: int, pixels: list) -> None:
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'wb') as f:
        f.write(_make_png(width, height, pixels))
    print(f"  ✓ {path}")

def solid(w: int, h: int, color: tuple) -> list:
    return [color] * (w * h)

def rect_border(w: int, h: int, fill: tuple, border: tuple, border_w: int = 1) -> list:
    pixels = []
    for y in range(h):
        for x in range(w):
            if x < border_w or x >= w - border_w or y < border_w or y >= h - border_w:
                pixels.append(border)
            else:
                pixels.append(fill)
    return pixels

def gradient_v(w: int, h: int, top: tuple, bottom: tuple) -> list:
    pixels = []
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] * (1-t) + bottom[0] * t)
        g = int(top[1] * (1-t) + bottom[1] * t)
        b = int(top[2] * (1-t) + bottom[2] * t)
        a = int(top[3] * (1-t) + bottom[3] * t)
        for x in range(w):
            pixels.append((r, g, b, a))
    return pixels

def checkerboard(w: int, h: int, c1: tuple, c2: tuple, size: int = 2) -> list:
    pixels = []
    for y in range(h):
        for x in range(w):
            if ((x // size) + (y // size)) % 2 == 0:
                pixels.append(c1)
            else:
                pixels.append(c2)
    return pixels

def blend(base: list, overlay: list, mask_color: tuple) -> list:
    return [overlay[i] if base[i] == mask_color else base[i] for i in range(len(base))]

# ===== COLOR PALETTE (SNES 15-bit style) =====
# Named colors used throughout

TRANSPARENT = (0, 0, 0, 0)
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
DARK_GRAY = (64, 64, 64, 255)
GRAY = (128, 128, 128, 255)
LIGHT_GRAY = (192, 192, 192, 255)

# Character palette tones
JAVIN_SCALE = (180, 80, 40, 255)      # Red-gold scales
JAVIN_ARMOR = (80, 60, 40, 255)       # Leather brown
FROSTBITE_SKIN = (100, 160, 100, 255) # Goblin green
FROSTBITE_GOGGLE = (80, 180, 220, 255)
FEI_FUR_DARK = (20, 20, 20, 255)      # Black panda
FEI_FUR_LIGHT = (240, 240, 240, 255)  # White panda
FLOOD_ROBE = (40, 100, 200, 255)      # Ice blue
FLOOD_SKIN = (200, 220, 255, 255)     # Pale blue
HANNAH_ROBE = (60, 20, 80, 255)       # Dark purple
HANNAH_HAT = (40, 15, 60, 255)
MICHAEL_CLERIC = (220, 200, 140, 255) # Cream/gold
MICHAEL_PLATE = (160, 170, 190, 255)  # Silver-blue
WARGHOUL_DARK = (30, 30, 50, 255)     # Dark undead
COOKIE_GREEN = (80, 140, 60, 255)     # Druid green
IRIS_BROWN = (140, 100, 60, 255)      # Nature tones
FRITZZIT_CAMO = (80, 100, 60, 255)    # Camouflage
CRANKPOT_FIRE = (220, 120, 30, 255)   # Fire orange
YIPP_FUR = (160, 140, 120, 255)       # Ratling tan

# UI colors
HP_RED = (200, 40, 40, 255)
HP_DARK = (80, 10, 10, 255)
MP_BLUE = (40, 80, 220, 255)
MP_DARK = (10, 20, 80, 255)
ATB_GOLD = (220, 180, 40, 255)
ATB_DARK = (80, 60, 10, 255)
UI_FRAME = (20, 20, 60, 255)
UI_FRAME_LIGHT = (80, 80, 160, 255)

# Enemy colors
KOBOLD_UNDEAD = (80, 140, 80, 255)    # Sickly green
KOBOLD_INFECTED = (120, 180, 80, 255)
SKELETON_BONE = (220, 200, 160, 255)
DRAGON_BLACK = (20, 20, 30, 255)
DRAGON_UNDEAD = (80, 40, 80, 255)
DRAGON_RED = (200, 40, 20, 255)
NECROMANCER_ROBE = (30, 10, 50, 255)
LICH_GLOW = (100, 30, 150, 255)

# Tile colors
STONE = (80, 80, 90, 255)
STONE_DARK = (50, 50, 60, 255)
STONE_LIGHT = (110, 110, 120, 255)
GRASS = (60, 140, 40, 255)
GRASS_DARK = (40, 100, 25, 255)
DIRT = (140, 100, 60, 255)
SAND = (220, 190, 120, 255)
SAND_DARK = (180, 150, 80, 255)
WATER = (30, 100, 200, 255)
FUNGAL = (120, 60, 140, 255)
BONE_TILE = (180, 160, 120, 255)

# ===== CHARACTER SPRITE GENERATOR =====

def make_character_sprite_sheet(char_id: str, palette: dict) -> list:
    """
    Creates a 16x24 character sprite with walk cycles.
    Returns a 64x96 sheet: 4 columns (directions) x 4 rows (frames)
    Actually returns as 64w x 96h pixel array.
    Simple blocky SNES-style figure.
    """
    W, H = 16, 24
    SHEET_W, SHEET_H = W * 4, H * 4  # 4 dirs x 4 frames
    pixels = [TRANSPARENT] * (SHEET_W * SHEET_H)

    body_color = palette.get("body", DARK_GRAY)
    skin_color = palette.get("skin", LIGHT_GRAY)
    hair_color = palette.get("hair", BLACK)
    weapon_color = palette.get("weapon", GRAY)
    armor_color = palette.get("armor", DARK_GRAY)
    highlight = palette.get("highlight", WHITE)

    def set_px(sheet_x, sheet_y, color):
        if 0 <= sheet_x < SHEET_W and 0 <= sheet_y < SHEET_H:
            pixels[sheet_y * SHEET_W + sheet_x] = color

    def draw_frame(dir_idx: int, frame_idx: int, leg_offset: int = 0):
        ox = dir_idx * W
        oy = frame_idx * H

        # Head (4x4 at center)
        for hx in range(6, 10):
            for hy in range(2, 6):
                set_px(ox + hx, oy + hy, skin_color)
        # Hair accent
        for hx in range(6, 10):
            set_px(ox + hx, oy + 2, hair_color)

        # Body/torso (8x8)
        for bx in range(4, 12):
            for by in range(6, 14):
                set_px(ox + bx, oy + by, body_color)
        # Armor shading
        for bx in range(4, 12):
            for by in range(6, 8):
                set_px(ox + bx, oy + by, armor_color)

        # Left leg
        ll_offset = leg_offset
        for lx in range(5, 8):
            for ly in range(14, 20 + ll_offset):
                set_px(ox + lx, oy + ly, armor_color)

        # Right leg
        rl_offset = -leg_offset
        for lx in range(9, 12):
            for ly in range(14, 20 + rl_offset):
                set_px(ox + lx, oy + ly, armor_color)

        # Feet
        for lx in range(4, 8):
            set_px(ox + lx, oy + 20 + ll_offset, body_color)
        for lx in range(8, 13):
            set_px(ox + lx, oy + 20 + rl_offset, body_color)

        # Arms
        for ax in range(2, 5):
            for ay in range(7, 14):
                set_px(ox + ax, oy + ay, armor_color)
        for ax in range(12, 15):
            for ay in range(7, 14):
                set_px(ox + ax, oy + ay, armor_color)

        # Weapon (right side)
        for wy in range(4, 16):
            set_px(ox + 14, oy + wy, weapon_color)

        # Highlight on head
        set_px(ox + 7, oy + 3, highlight)
        set_px(ox + 8, oy + 3, highlight)

    # Draw all 4 directions x 4 frames
    leg_offsets = [0, 2, 0, -2]  # Walk animation
    for direction in range(4):  # down, left, right, up
        for frame in range(4):
            draw_frame(direction, frame, leg_offsets[frame])

    return pixels

# ===== ENEMY SPRITE GENERATOR =====

def make_16x16_enemy(primary: tuple, secondary: tuple, eye_color: tuple = None) -> list:
    if eye_color is None:
        eye_color = WHITE
    pixels = [TRANSPARENT] * (16 * 16)
    def s(x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            pixels[y * 16 + x] = c

    # Body oval
    for y in range(3, 13):
        for x in range(2, 14):
            if (x-8)**2 * 0.3 + (y-8)**2 * 0.5 < 25:
                s(x, y, primary)
    # Secondary accent
    for x in range(4, 12):
        for y in range(5, 9):
            s(x, y, secondary)
    # Eyes
    s(5, 6, eye_color)
    s(10, 6, eye_color)
    s(5, 7, BLACK)
    s(10, 7, BLACK)
    # Outline
    for y in range(16):
        for x in range(16):
            if pixels[y*16+x] != TRANSPARENT:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < 16 and 0 <= ny < 16 and pixels[ny*16+nx] == TRANSPARENT:
                        pixels[ny*16+nx] = (0,0,0,180)
    return pixels

def make_32x32_enemy(colors: list) -> list:
    """32x32 enemy (boss mini)"""
    W, H = 32, 32
    pixels = [TRANSPARENT] * (W * H)
    def s(x, y, c):
        if 0 <= x < W and 0 <= y < H:
            pixels[y * W + x] = c

    primary = colors[0]
    secondary = colors[1] if len(colors) > 1 else DARK_GRAY
    accent = colors[2] if len(colors) > 2 else WHITE

    # Large body
    for y in range(4, 28):
        for x in range(3, 29):
            if (x-16)**2 * 0.3 + (y-16)**2 * 0.4 < 120:
                s(x, y, primary)
    # Belly
    for y in range(10, 22):
        for x in range(10, 22):
            if (x-16)**2 + (y-16)**2 < 40:
                s(x, y, secondary)
    # Head area
    for y in range(2, 12):
        for x in range(8, 24):
            s(x, y, primary)
    # Eyes
    for px, py in [(12, 6), (20, 6)]:
        s(px, py, WHITE)
        s(px+1, py, WHITE)
        s(px, py+1, accent)
        s(px+1, py+1, BLACK)
    # Outline
    for y in range(H):
        for x in range(W):
            if pixels[y*W+x] != TRANSPARENT:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < W and 0 <= ny < H and pixels[ny*W+nx] == TRANSPARENT:
                        pixels[ny*W+nx] = (0,0,0,180)
    return pixels

def make_64x64_boss(colors: list, boss_type: str = "dragon") -> list:
    W, H = 64, 64
    pixels = [TRANSPARENT] * (W * H)
    def s(x, y, c):
        if 0 <= x < W and 0 <= y < H:
            pixels[y * W + x] = c

    primary = colors[0]
    secondary = colors[1] if len(colors) > 1 else DARK_GRAY
    accent = colors[2] if len(colors) > 2 else WHITE

    if boss_type in ["dragon", "undead_dragon", "red_dragon"]:
        # Dragon body
        for y in range(15, 55):
            for x in range(10, 54):
                if (x-32)**2 * 0.2 + (y-35)**2 * 0.3 < 280:
                    s(x, y, primary)
        # Head
        for y in range(5, 25):
            for x in range(5, 40):
                if (x-20)**2 * 0.2 + (y-15)**2 * 0.4 < 180:
                    s(x, y, primary)
        # Neck
        for y in range(18, 30):
            for x in range(10, 28):
                s(x, y, primary)
        # Wing shape
        for y in range(10, 45):
            for x in range(40, 62):
                wing_h = min(y, 45) - max(y, 10)
                if (x - 40) < (45 - y) * 0.8:
                    s(x, y, secondary)
        # Belly scales
        for y in range(25, 50):
            for x in range(20, 50):
                if (x-35)**2 + (y-38)**2 < 120:
                    s(x, y, secondary)
        # Eyes (large, glowing)
        for ex, ey in [(15, 13), (28, 11)]:
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if dx*dx + dy*dy <= 4:
                        s(ex+dx, ey+dy, accent)
            s(ex, ey, BLACK)
        # Horns
        for i in range(8):
            s(12 + i//2, 5 - i, primary)
            s(24 + i//2, 3 - i//2, primary)
    elif boss_type == "lich":
        # Lich (tall robed skeleton)
        # Robe
        for y in range(20, 62):
            for x in range(15, 49):
                if abs(x - 32) < 17 - (y - 20) * 0.1:
                    s(x, y, primary)
        # Skull head
        for y in range(5, 22):
            for x in range(18, 46):
                if (x-32)**2 * 0.3 + (y-13)**2 * 0.5 < 70:
                    s(x, y, (220, 200, 160, 255))
        # Eye sockets (glowing)
        for ex, ey in [(25, 14), (39, 14)]:
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if dx*dx + dy*dy <= 4:
                        s(ex+dx, ey+dy, accent)
            s(ex, ey, LICH_GLOW)
        # Crown/horns
        for i in range(5):
            s(24 + i*4, 3 + (i%2)*2, (180, 150, 20, 255))
        # Staff
        for y in range(10, 60):
            s(10, y, (80, 60, 40, 255))
        s(8, 10, accent)
        s(10, 10, accent)
        s(12, 10, accent)
        # Decay details on robe
        for y in range(25, 55, 5):
            for x in range(18, 46, 4):
                s(x, y, secondary)

    # Outline
    for y in range(H):
        for x in range(W):
            if pixels[y*W+x] != TRANSPARENT:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < W and 0 <= ny < H and pixels[ny*W+nx] == TRANSPARENT:
                        pixels[ny*W+nx] = (0,0,0,200)
    return pixels

# ===== TILESET GENERATOR =====

def make_tileset_16x16(tiles: list) -> list:
    """tiles = list of (fill_color, accent_color, style_name)
    Returns a horizontal strip of 16x16 tiles."""
    count = len(tiles)
    W = 16 * count
    H = 16
    pixels = [TRANSPARENT] * (W * H)

    for i, (fill, accent, style) in enumerate(tiles):
        ox = i * 16
        base = rect_border(16, 16, fill, accent, 1)

        if style == "stone":
            # Crack lines
            for x in range(2, 14, 4):
                for y in range(2, 14):
                    base[y * 16 + x] = tuple(max(0, c-20) for c in fill[:3]) + (255,)
        elif style == "grass":
            # Grass tufts at top
            for x in range(2, 14, 3):
                base[1 * 16 + x] = (80, 180, 40, 255)
                base[2 * 16 + x] = (60, 160, 30, 255)
        elif style == "sand":
            # Ripple effect
            for y in range(4, 12, 4):
                for x in range(1, 15):
                    base[y * 16 + x] = tuple(min(255, c+20) for c in fill[:3]) + (255,)
        elif style == "fungal":
            # Spots
            for fx, fy in [(4,4),(8,8),(12,5),(6,11)]:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if 0 <= fx+dx < 16 and 0 <= fy+dy < 16:
                            base[(fy+dy)*16 + (fx+dx)] = (180, 80, 200, 255)
        elif style == "dark_stone":
            for x in range(0, 16, 8):
                for y in range(0, 16, 4):
                    base[y*16 + x] = tuple(max(0, c-10) for c in fill[:3]) + (255,)

        for y in range(16):
            for x in range(16):
                pixels[y * W + (ox + x)] = base[y * 16 + x]

    return pixels

# ===== BATTLE BACKGROUND GENERATOR =====

def make_battle_bg(name: str) -> tuple:
    """Returns (width=256, height=112, pixels)"""
    W, H = 256, 112

    BG_CONFIGS = {
        "warren_stone_tunnel": {
            "sky": (30, 25, 35, 255),
            "ground": (60, 55, 65, 255),
            "detail": (45, 40, 50, 255),
        },
        "dungeon": {
            "sky": (20, 15, 25, 255),
            "ground": (50, 45, 55, 255),
            "detail": (35, 30, 40, 255),
        },
        "forest": {
            "sky": (60, 120, 200, 255),
            "ground": (50, 100, 30, 255),
            "detail": (40, 140, 40, 255),
        },
        "imperial_city_streets": {
            "sky": (100, 140, 200, 255),
            "ground": (100, 90, 80, 255),
            "detail": (120, 110, 100, 255),
        },
        "desert_ruins": {
            "sky": (220, 160, 80, 255),
            "ground": (200, 170, 100, 255),
            "detail": (180, 150, 80, 255),
        },
        "dragon_lair_volcanic": {
            "sky": (60, 20, 10, 255),
            "ground": (40, 20, 10, 255),
            "detail": (180, 60, 10, 255),
        },
        "dragon_lair_undead": {
            "sky": (20, 10, 30, 255),
            "ground": (30, 15, 40, 255),
            "detail": (80, 30, 100, 255),
        },
        "catacomb": {
            "sky": (15, 10, 20, 255),
            "ground": (40, 35, 45, 255),
            "detail": (60, 50, 70, 255),
        },
        "necromancer_sanctum": {
            "sky": (10, 5, 20, 255),
            "ground": (25, 15, 35, 255),
            "detail": (100, 30, 140, 255),
        },
        "capitol_city": {
            "sky": (80, 60, 40, 255),
            "ground": (80, 70, 60, 255),
            "detail": (100, 80, 60, 255),
        },
        "slaver_island_docks": {
            "sky": (40, 80, 140, 255),
            "ground": (60, 45, 30, 255),
            "detail": (50, 70, 90, 255),
        },
    }

    config = BG_CONFIGS.get(name, BG_CONFIGS["dungeon"])
    sky_color = config["sky"]
    ground_color = config["ground"]
    detail_color = config["detail"]

    pixels = []
    ground_line = int(H * 0.55)

    for y in range(H):
        for x in range(W):
            # Sky/background gradient
            if y < ground_line:
                t = y / ground_line
                r = int(sky_color[0] * (1-t*0.3))
                g = int(sky_color[1] * (1-t*0.3))
                b = int(sky_color[2] * (1-t*0.3))
                color = (r, g, b, 255)
            else:
                # Ground with slight perspective darkening
                t = (y - ground_line) / (H - ground_line)
                r = int(ground_color[0] * (1 - t * 0.3))
                g = int(ground_color[1] * (1 - t * 0.3))
                b = int(ground_color[2] * (1 - t * 0.3))
                color = (r, g, b, 255)

            # Ground line
            if y == ground_line:
                color = detail_color

            # Detail elements based on background type
            if name == "forest":
                # Trees
                for tx in range(0, W, 40):
                    if y < ground_line - 20 and abs(x - tx) < 15:
                        tree_h = ground_line - y
                        if abs(x - tx) < min(15, tree_h // 3):
                            color = (40, 120, 30, 255)
            elif name == "warren_stone_tunnel" or name == "dungeon":
                # Stone wall pattern
                if y < ground_line:
                    bx = (x // 16) + (y // 8) % 2
                    by = y // 8
                    if x % 16 == 0 or y % 8 == 0:
                        color = tuple(max(0, c-15) for c in color[:3]) + (255,)
            elif name == "dragon_lair_volcanic":
                # Lava cracks
                if y > ground_line and (x + y*2) % 20 < 2:
                    color = (220, 80, 10, 255)
            elif name == "catacomb" or name == "necromancer_sanctum":
                # Candle glow points
                for cx in range(20, W, 60):
                    dist = abs(x - cx)
                    if dist < 8 and abs(y - (ground_line - 15)) < 8:
                        glow = max(0, 8 - dist)
                        color = (
                            min(255, color[0] + glow * 15),
                            min(255, color[1] + glow * 8),
                            min(255, color[2] + glow * 2),
                            255
                        )

            pixels.append(color)

    return W, H, pixels

# ===== UI ELEMENT GENERATOR =====

def make_ui_panel(w: int, h: int) -> list:
    """Dark blue pixel art UI panel with decorative corners"""
    pixels = [TRANSPARENT] * (w * h)
    def s(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            pixels[y * w + x] = c

    # Fill background
    for y in range(h):
        for x in range(w):
            s(x, y, (10, 10, 40, 220))

    # Outer border
    for x in range(w):
        s(x, 0, UI_FRAME_LIGHT)
        s(x, h-1, UI_FRAME_LIGHT)
    for y in range(h):
        s(0, y, UI_FRAME_LIGHT)
        s(w-1, y, UI_FRAME_LIGHT)

    # Inner border
    for x in range(2, w-2):
        s(x, 2, UI_FRAME)
        s(x, h-3, UI_FRAME)
    for y in range(2, h-2):
        s(2, y, UI_FRAME)
        s(w-3, y, UI_FRAME)

    # Corner decorations
    for corner_x, corner_y in [(0,0),(w-4,0),(0,h-4),(w-4,h-4)]:
        s(corner_x+1, corner_y+1, WHITE)
        s(corner_x+2, corner_y+1, LIGHT_GRAY)
        s(corner_x+1, corner_y+2, LIGHT_GRAY)

    return pixels

def make_stat_bar(w: int, h: int, bar_type: str) -> list:
    """HP/MP/ATB bar sprite"""
    colors = {
        "hp": (HP_RED, HP_DARK),
        "mp": (MP_BLUE, MP_DARK),
        "atb": (ATB_GOLD, ATB_DARK),
    }
    fill, dark = colors.get(bar_type, (GRAY, DARK_GRAY))
    pixels = solid(w, h, dark)
    # Fill 75% to show example
    fill_w = int(w * 0.75)
    for y in range(1, h-1):
        for x in range(1, fill_w):
            if x < w - 1:
                pixels[y * w + x] = fill
    # Highlight
    for x in range(1, fill_w):
        if x < w - 1:
            pixels[1 * w + x] = tuple(min(255, c+60) for c in fill[:3]) + (255,)
    return pixels

def make_status_icon(status: str, size: int = 12) -> list:
    """Small status effect icon"""
    colors = {
        "poison": (120, 40, 160, 255),
        "sleep": (80, 80, 200, 255),
        "paralysis": (200, 200, 40, 255),
        "blind": (40, 40, 40, 255),
        "silence": (160, 160, 160, 255),
        "slow": (40, 40, 140, 255),
        "haste": (220, 180, 40, 255),
        "berserk": (220, 40, 40, 255),
        "confuse": (180, 80, 180, 255),
        "burn": (220, 100, 20, 255),
        "bubble": (80, 180, 220, 255),
    }
    base_color = colors.get(status, GRAY)
    pixels = [TRANSPARENT] * (size * size)

    # Circle shape
    cx, cy = size // 2, size // 2
    for y in range(size):
        for x in range(size):
            d = (x - cx)**2 + (y - cy)**2
            if d <= (size//2 - 1)**2:
                pixels[y * size + x] = base_color
            elif d <= (size//2)**2:
                pixels[y * size + x] = BLACK

    # Letter abbreviation in center (simplified - just a dot pattern)
    pixels[cy * size + cx] = WHITE
    pixels[(cy-1) * size + cx] = WHITE

    return pixels

def make_cursor(w: int = 8, h: int = 12) -> list:
    """Arrow cursor sprite"""
    pixels = [TRANSPARENT] * (w * h)
    def s(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            pixels[y * w + x] = c

    # Arrow pointing right
    for y in range(h):
        width_at_y = min(y + 1, h - y, w)
        for x in range(width_at_y):
            s(x, y, WHITE)
        # Outline
        if width_at_y > 0:
            s(width_at_y, y, BLACK)

    return pixels

def make_save_point_crystal(size: int = 16) -> list:
    """Glowing crystal save point"""
    pixels = [TRANSPARENT] * (size * size)
    def s(x, y, c):
        if 0 <= x < size and 0 <= y < size:
            pixels[y * size + x] = c

    cx, cy = size // 2, size // 2
    crystal_color = (80, 180, 255, 255)
    glow_color = (120, 200, 255, 200)
    inner = (200, 230, 255, 255)

    # Outer glow
    for y in range(size):
        for x in range(size):
            d = math.sqrt((x-cx)**2 + (y-cy)**2)
            if d < size * 0.45:
                s(x, y, glow_color)

    # Crystal diamond shape
    for y in range(size):
        for x in range(size):
            if abs(x - cx) + abs(y - cy) < size * 0.35:
                s(x, y, crystal_color)

    # Inner bright
    for y in range(size):
        for x in range(size):
            if abs(x - cx) + abs(y - cy) < size * 0.2:
                s(x, y, inner)

    # Sparkle
    s(cx - 2, cy - 2, WHITE)
    s(cx + 2, cy + 2, WHITE)
    s(cx, cy - 3, WHITE)

    # Outline
    for y in range(size):
        for x in range(size):
            if pixels[y*size+x] != TRANSPARENT:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < size and 0 <= ny < size and pixels[ny*size+nx] == TRANSPARENT:
                        pixels[ny*size+nx] = (40, 120, 200, 255)

    return pixels

def make_treasure_chest(w: int = 16, h: int = 14, is_open: bool = False) -> list:
    pixels = [TRANSPARENT] * (w * h)
    def s(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            pixels[y * w + x] = c

    chest_gold = (200, 160, 40, 255)
    chest_dark = (80, 60, 10, 255)
    chest_wood = (120, 80, 30, 255)
    lock_silver = (180, 180, 200, 255)

    if not is_open:
        # Closed chest
        # Lid
        for y in range(3, 7):
            for x in range(1, 15):
                s(x, y, chest_wood)
        for x in range(1, 15):
            s(3, x, chest_gold) if x < 4 else None  # Rim
            s(3, x, chest_gold) if x > 6 else None

        # Body
        for y in range(7, 13):
            for x in range(1, 15):
                s(x, y, chest_wood)

        # Gold trim
        for x in range(1, 15):
            s(x, 3, chest_gold)
            s(x, 7, chest_gold)
            s(x, 12, chest_gold)
        for y in range(3, 13):
            s(1, y, chest_gold)
            s(14, y, chest_gold)

        # Lock
        for y in range(8, 12):
            for x in range(6, 10):
                s(x, y, lock_silver)
        s(7, 9, chest_dark)
        s(8, 9, chest_dark)
    else:
        # Open chest (lid tilted back)
        for y in range(1, 5):
            for x in range(1, 15):
                s(x, y, chest_wood)
        for x in range(1, 15):
            s(1, x, chest_gold) if x < 2 else None
        # Body
        for y in range(7, 13):
            for x in range(1, 15):
                s(x, y, chest_wood)
        # Interior glow
        for y in range(8, 12):
            for x in range(3, 13):
                s(x, y, (240, 200, 80, 255))

    return pixels

# ===== OVERWORLD MAP ICONS =====

def make_overworld_icon(icon_type: str, size: int = 16) -> list:
    pixels = [TRANSPARENT] * (size * size)
    def s(x, y, c):
        if 0 <= x < size and 0 <= y < size:
            pixels[y * size + x] = c

    half = size // 2
    configs = {
        "town": (LIGHT_GRAY, (180, 140, 80, 255)),
        "city": ((200, 180, 140, 255), (150, 120, 60, 255)),
        "dungeon": (STONE_DARK, DARK_GRAY),
        "forest": (GRASS, GRASS_DARK),
        "desert": (SAND, SAND_DARK),
        "mountain": (GRAY, DARK_GRAY),
        "army_camp": ((180, 40, 40, 255), (120, 20, 20, 255)),
        "warren": (STONE_DARK, FUNGAL),
        "dragon_lair": (DRAGON_BLACK, (200, 60, 10, 255)),
    }
    primary, secondary = configs.get(icon_type, (GRAY, DARK_GRAY))

    if icon_type in ["town", "city"]:
        # Building silhouette
        for y in range(4, size-2):
            for x in range(2, size-2):
                s(x, y, primary)
        # Roof
        for y in range(1, 6):
            for x in range(half - y, half + y):
                s(x, y, secondary)
        # Door
        for y in range(10, size-2):
            for x in range(half-2, half+2):
                s(x, y, secondary)
    elif icon_type == "dungeon":
        # Cave entrance
        for y in range(4, size-2):
            for x in range(2, size-2):
                s(x, y, primary)
        # Dark entrance hole
        cx, cy = half, size - 4
        for dx in range(-3, 4):
            for dy in range(-3, 1):
                if dx*dx*0.5 + dy*dy < 9:
                    s(cx+dx, cy+dy, BLACK)
    elif icon_type == "forest":
        # Tree silhouettes
        for tx in [4, half, size-4]:
            for y in range(2, size-4):
                for x in range(tx-3, tx+3):
                    if abs(x-tx) <= (size-4-y)//2:
                        s(x, y, primary)
            s(tx, size-4, secondary)
            s(tx, size-3, secondary)
    elif icon_type == "dragon_lair":
        # Skull/cave with fire
        for y in range(4, size-2):
            for x in range(2, size-2):
                s(x, y, primary)
        # Fire glow
        for y in range(8, size-3):
            for x in range(half-2, half+2):
                s(x, y, secondary)
    elif icon_type == "mountain":
        # Mountain peaks
        for peak_x in [5, 11]:
            for y in range(2, size-2):
                for x in range(peak_x - (y-2)//2, peak_x + (y-2)//2 + 1):
                    s(x, y, primary)
        # Snow cap
        for peak_x in [5, 11]:
            for y in range(2, 6):
                for x in range(peak_x - (y-2)//4, peak_x + (y-2)//4 + 1):
                    s(x, y, WHITE)

    # Outline
    for y in range(size):
        for x in range(size):
            if pixels[y*size+x] != TRANSPARENT:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < size and 0 <= ny < size and pixels[ny*size+nx] == TRANSPARENT:
                        pixels[ny*size+nx] = BLACK

    return pixels

# ===== SPELL EFFECT SPRITES =====

def make_spell_effect(element: str, size: int = 16) -> list:
    pixels = [TRANSPARENT] * (size * size)
    def s(x, y, c):
        if 0 <= x < size and 0 <= y < size:
            pixels[y * size + x] = c

    cx, cy = size // 2, size // 2

    if element == "fire":
        # Flame burst
        flame_colors = [(220, 180, 40, 255), (220, 100, 20, 255), (200, 40, 10, 255)]
        for y in range(size):
            for x in range(size):
                d = math.sqrt((x-cx)**2 + (y-cy)**2)
                if d < 7:
                    ci = min(2, int(d / 2.5))
                    s(x, y, flame_colors[ci])
        # Bright center
        s(cx, cy, WHITE)
        s(cx-1, cy, (255, 240, 200, 255))

    elif element == "ice" or element == "water":
        # Ice shard / snowflake
        shard_color = (120, 200, 255, 255)
        ice_inner = (200, 240, 255, 255)
        for i in range(6):
            angle = i * math.pi / 3
            for r in range(1, 7):
                px = int(cx + r * math.cos(angle))
                py = int(cy + r * math.sin(angle))
                s(px, py, shard_color)
        # Center
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx*dx + dy*dy <= 4:
                    s(cx+dx, cy+dy, ice_inner)
        s(cx, cy, WHITE)

    elif element == "thunder":
        # Lightning bolt
        bolt = (240, 240, 80, 255)
        bolt_core = WHITE
        pts = [(cx+2, 1), (cx, cy-2), (cx+3, cy-2), (cx-1, cy+3), (cx+2, cy+3), (cx, size-2)]
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i+1]
            dx_s = 1 if x2 > x1 else -1
            dy_s = 1 if y2 > y1 else -1
            x, y = x1, y1
            while x != x2 or y != y2:
                s(x, y, bolt)
                s(x+1, y, bolt)
                if x != x2: x += dx_s
                if y != y2: y += dy_s
            s(x, y, bolt_core)

    elif element == "light" or element == "holy":
        # Light burst
        holy_gold = (255, 240, 100, 255)
        for y in range(size):
            for x in range(size):
                d = math.sqrt((x-cx)**2 + (y-cy)**2)
                # Rays
                angle = math.atan2(y-cy, x-cx)
                ray = abs(math.sin(angle * 4)) > 0.7
                if d < 3 or (d < 7 and ray):
                    s(x, y, holy_gold)
        s(cx, cy, WHITE)

    elif element == "darkness":
        # Shadow pulse
        for y in range(size):
            for x in range(size):
                d = math.sqrt((x-cx)**2 + (y-cy)**2)
                if 3 < d < 7:
                    s(x, y, (60, 20, 80, 200))
                elif d <= 3:
                    s(x, y, (100, 40, 120, 255))

    elif element == "earth":
        # Rock shatter
        rock_colors = [(80, 60, 40, 255), (100, 80, 50, 255), (120, 90, 60, 255)]
        for rock_cx, rock_cy, rsize in [(4, 4, 3), (10, 6, 2), (6, 11, 4), (12, 11, 3)]:
            for y in range(rock_cy - rsize, rock_cy + rsize):
                for x in range(rock_cx - rsize, rock_cx + rsize):
                    if abs(x-rock_cx) + abs(y-rock_cy) < rsize:
                        s(x, y, rock_colors[rsize % 3])

    elif element == "psychic":
        # Purple wave distortion rings
        psychic_color = (180, 60, 220, 255)
        psychic_inner = (220, 120, 255, 255)
        for ring_r in [3, 5, 7]:
            for y in range(size):
                for x in range(size):
                    d = math.sqrt((x-cx)**2 + (y-cy)**2)
                    if abs(d - ring_r) < 0.8:
                        s(x, y, psychic_color)
        s(cx, cy, psychic_inner)
        s(cx-1, cy, psychic_inner)
        s(cx+1, cy, psychic_inner)

    elif element == "heal":
        # Green sparkle
        heal_green = (40, 220, 80, 255)
        for spark_x, spark_y in [(cx, cy-5), (cx-4, cy-3), (cx+4, cy-3), (cx-5, cy+1), (cx+5, cy+1)]:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    s(spark_x+dx, spark_y+dy, heal_green)
            s(spark_x, spark_y, WHITE)
        # Cross in center
        for i in range(-3, 4):
            s(cx+i, cy, heal_green)
            s(cx, cy+i, heal_green)
        s(cx, cy, WHITE)

    return pixels

# ===== PORTRAIT FRAME =====

def make_portrait_frame(size: int = 32) -> list:
    """Character portrait border frame"""
    pixels = [TRANSPARENT] * (size * size)
    def s(x, y, c):
        if 0 <= x < size and 0 <= y < size:
            pixels[y * size + x] = c

    gold = (200, 160, 40, 255)
    dark_gold = (100, 80, 20, 255)
    inner = (20, 15, 30, 220)

    # Fill
    for y in range(size):
        for x in range(size):
            s(x, y, inner)

    # Ornate border
    for x in range(size):
        s(x, 0, gold); s(x, 1, dark_gold)
        s(x, size-1, gold); s(x, size-2, dark_gold)
    for y in range(size):
        s(0, y, gold); s(1, y, dark_gold)
        s(size-1, y, gold); s(size-2, y, dark_gold)

    # Corner gems
    for cx2, cy2 in [(1,1),(size-2,1),(1,size-2),(size-2,size-2)]:
        s(cx2, cy2, WHITE)
        s(cx2+1, cy2, (200, 180, 255, 255))
        s(cx2, cy2+1, (200, 180, 255, 255))

    return pixels


# ===== MAIN GENERATION =====

def main():
    print("Generating pixel art assets for 'There Will Be Kobolds'...")
    print("=" * 60)

    # ===== CHARACTER SPRITES =====
    print("\n[Characters]")
    char_palettes = {
        "javin": {"body": JAVIN_ARMOR, "skin": JAVIN_SCALE, "hair": (120,60,20,255), "weapon": (140,140,160,255), "armor": JAVIN_ARMOR, "highlight": (220,180,80,255)},
        "frostbite": {"body": FROSTBITE_SKIN, "skin": FROSTBITE_SKIN, "hair": (20,20,20,255), "weapon": (80,80,100,255), "armor": (60,80,60,255), "highlight": FROSTBITE_GOGGLE},
        "fei": {"body": FEI_FUR_DARK, "skin": FEI_FUR_LIGHT, "hair": FEI_FUR_DARK, "weapon": (140,100,40,255), "armor": FEI_FUR_DARK, "highlight": WHITE},
        "flood": {"body": FLOOD_ROBE, "skin": FLOOD_SKIN, "hair": (180,220,255,255), "weapon": (100,160,220,255), "armor": FLOOD_ROBE, "highlight": (180,220,255,255)},
        "hannah": {"body": HANNAH_ROBE, "skin": (220,180,160,255), "hair": BLACK, "weapon": (80,40,120,255), "armor": HANNAH_ROBE, "highlight": (180,100,220,255)},
        "michael": {"body": MICHAEL_CLERIC, "skin": (220,190,160,255), "hair": (180,140,80,255), "weapon": (200,200,220,255), "armor": MICHAEL_PLATE, "highlight": (255,240,180,255)},
        "warghoul": {"body": WARGHOUL_DARK, "skin": (60,80,60,255), "hair": BLACK, "weapon": (80,60,80,255), "armor": WARGHOUL_DARK, "highlight": (100,100,140,255)},
        "cookie": {"body": COOKIE_GREEN, "skin": (220,180,140,255), "hair": (180,120,60,255), "weapon": (100,140,80,255), "armor": COOKIE_GREEN, "highlight": (200,220,100,255)},
        "iris": {"body": IRIS_BROWN, "skin": (220,190,150,255), "hair": (100,60,40,255), "weapon": (80,100,60,255), "armor": IRIS_BROWN, "highlight": (220,180,100,255)},
        "fritzzit": {"body": FRITZZIT_CAMO, "skin": FROSTBITE_SKIN, "hair": (40,40,20,255), "weapon": (60,60,60,255), "armor": FRITZZIT_CAMO, "highlight": (100,120,80,255)},
        "crankpot": {"body": (60,40,30,255), "skin": (100,140,80,255), "hair": BLACK, "weapon": CRANKPOT_FIRE, "armor": (60,40,30,255), "highlight": CRANKPOT_FIRE},
        "yipp": {"body": (80,60,80,255), "skin": YIPP_FUR, "hair": (80,60,80,255), "weapon": (60,40,80,255), "armor": (80,60,80,255), "highlight": (180,140,180,255)},
        "kella": {"body": (80,20,20,255), "skin": (160,80,60,255), "hair": (40,10,10,255), "weapon": (200,160,40,255), "armor": (80,20,20,255), "highlight": (220,180,40,255)},
        "orisia": {"body": (140,120,80,255), "skin": (220,180,140,255), "hair": (60,40,20,255), "weapon": (120,100,60,255), "armor": (140,120,80,255), "highlight": (200,160,80,255)},
    }

    for char_id, palette in char_palettes.items():
        path = f"sprites/characters/{char_id}.png"
        pix = make_character_sprite_sheet(char_id, palette)
        save_png(path, 64, 96, pix)

    # ===== ENEMY SPRITES =====
    print("\n[Enemies - 16x16]")
    small_enemies = {
        "kobold": (KOBOLD_UNDEAD, (60,100,60,255), (200,200,100,255)),
        "infected_kobold": (KOBOLD_INFECTED, (80,120,40,255), (220,220,80,255)),
        "skeleton": (SKELETON_BONE, (180,160,120,255), BLACK),
        "zombie": (KOBOLD_UNDEAD, (40,80,40,255), (180,200,100,255)),
        "fungal_deer": ((120,80,60,255), (160,60,140,255), (200,180,100,255)),
        "lycanthrope_small": ((100,80,60,255), (60,40,20,255), (220,180,100,255)),
        "vampire_bat": ((40,20,60,255), (80,40,100,255), (220,60,60,255)),
        "desert_wraith": ((60,40,80,255), (100,60,120,255), (180,60,220,255)),
        "cultist": ((40,20,60,255), (60,40,80,255), (200,160,40,255)),
        "sand_scorpion": ((160,120,40,255), (200,160,60,255), BLACK),
    }
    for enemy_id, (primary, secondary, eye) in small_enemies.items():
        path = f"sprites/enemies/{enemy_id}.png"
        save_png(path, 16, 16, make_16x16_enemy(primary, secondary, eye))

    print("\n[Enemies - 32x32]")
    medium_enemies = {
        "jerod_fungal_boss": [(80, 140, 40, 255), (160, 60, 180, 255), (220, 200, 40, 255)],
        "captain_donald": [(60, 80, 120, 255), (40, 60, 100, 255), (220, 180, 40, 255)],
        "skeleton_warrior": [(SKELETON_BONE[0], SKELETON_BONE[1], SKELETON_BONE[2], 255), (160, 140, 100, 255), BLACK],
        "zombie_orc": [(60, 100, 50, 255), (40, 70, 30, 255), (180, 200, 80, 255)],
    }
    for enemy_id, colors in medium_enemies.items():
        path = f"sprites/enemies/{enemy_id}.png"
        save_png(path, 32, 32, make_32x32_enemy(colors))

    print("\n[Enemies - 64x64 Bosses]")
    bosses = {
        "black_dragon": ([DRAGON_BLACK, (40, 30, 50, 255), (80, 80, 220, 255)], "dragon"),
        "undead_dragon": ([(60, 30, 70, 255), (40, 20, 50, 255), (180, 80, 220, 255)], "undead_dragon"),
        "necromancer_lich": ([NECROMANCER_ROBE, (50, 25, 70, 255), LICH_GLOW], "lich"),
        "kella_double_infected": ([(100, 30, 30, 255), (80, 60, 40, 255), (220, 80, 40, 255)], "dragon"),
        "infected_red_dragon": ([DRAGON_RED, (150, 30, 10, 255), (220, 160, 40, 255)], "dragon"),
    }
    for boss_id, (colors, boss_type) in bosses.items():
        path = f"sprites/enemies/{boss_id}.png"
        save_png(path, 64, 64, make_64x64_boss(colors, boss_type))

    # ===== TILESETS =====
    print("\n[Tilesets]")
    tilesets = {
        "warren": [
            (STONE, STONE_LIGHT, "stone"),
            (STONE_DARK, STONE, "dark_stone"),
            (DIRT, (120,90,55,255), "stone"),
            (FUNGAL, (100,40,120,255), "fungal"),
            ((40,30,50,255), (60,45,70,255), "dark_stone"),
            ((80,70,90,255), STONE_LIGHT, "stone"),
        ],
        "surface_forest": [
            (GRASS, GRASS_DARK, "grass"),
            (GRASS_DARK, (30,80,20,255), "grass"),
            (DIRT, (100,70,40,255), "stone"),
            ((60,50,30,255), (40,30,20,255), "stone"),
            (WATER, (20,80,180,255), "stone"),
            ((100,140,80,255), (80,120,60,255), "grass"),
        ],
        "imperial_city": [
            ((120,110,100,255), (100,90,80,255), "stone"),
            ((140,130,120,255), (160,150,140,255), "stone"),
            ((80,70,60,255), (60,50,40,255), "dark_stone"),
            ((100,95,90,255), (120,115,110,255), "stone"),
            ((60,55,50,255), (50,45,40,255), "dark_stone"),
            ((160,150,140,255), (180,170,160,255), "stone"),
        ],
        "desert": [
            (SAND, SAND_DARK, "sand"),
            (SAND_DARK, (160,130,60,255), "sand"),
            ((200,160,80,255), (180,140,60,255), "sand"),
            ((160,130,90,255), (140,110,70,255), "stone"),
            ((180,150,80,255), (200,170,100,255), "sand"),
            (STONE, STONE_DARK, "stone"),
        ],
        "catacomb": [
            (STONE_DARK, (30,25,35,255), "dark_stone"),
            ((40,35,45,255), (20,15,25,255), "dark_stone"),
            (BONE_TILE, (160,140,100,255), "stone"),
            ((25,20,30,255), (35,30,40,255), "dark_stone"),
            ((50,40,55,255), (30,25,35,255), "stone"),
            ((60,50,65,255), (40,35,45,255), "stone"),
        ],
        "overworld": [
            (GRASS, GRASS_DARK, "grass"),
            ((30,80,20,255), (20,60,15,255), "grass"),
            (WATER, (20,80,180,255), "stone"),
            (STONE, STONE_DARK, "stone"),
            (SAND, SAND_DARK, "sand"),
            ((200,210,230,255), (180,190,210,255), "stone"),  # Snow
            ((100,80,60,255), DIRT, "stone"),  # Road
            (GRAY, DARK_GRAY, "stone"),  # Mountain
        ],
    }

    for tileset_name, tiles in tilesets.items():
        path = f"tilesets/tileset_{tileset_name}.png"
        count = len(tiles)
        pixels = make_tileset_16x16(tiles)
        save_png(path, 16 * count, 16, pixels)

    # ===== BATTLE BACKGROUNDS =====
    print("\n[Battle Backgrounds]")
    bg_names = [
        "warren_stone_tunnel", "dungeon", "forest", "imperial_city_streets",
        "city_sewer", "desert_ruins", "dragon_lair_volcanic", "dragon_lair_undead",
        "catacomb", "necromancer_sanctum", "capitol_city", "slaver_island_docks",
    ]
    for bg_name in bg_names:
        W, H, pixels = make_battle_bg(bg_name)
        save_png(f"backgrounds/battle_{bg_name}.png", W, H, pixels)

    # ===== UI SPRITES =====
    print("\n[UI Sprites]")

    # Panel frame (various sizes)
    for w, h in [(256, 40), (128, 80), (80, 60), (200, 100)]:
        save_png(f"sprites/ui/panel_{w}x{h}.png", w, h, make_ui_panel(w, h))

    # Stat bars
    for bar_type in ["hp", "mp", "atb"]:
        for w in [50, 80, 100]:
            save_png(f"sprites/ui/bar_{bar_type}_{w}.png", w, 7,
                     make_stat_bar(w, 7, bar_type))

    # Status effect icons
    for status in ["poison","sleep","paralysis","blind","silence","slow","haste","berserk","confuse","burn","bubble"]:
        save_png(f"sprites/ui/status_{status}.png", 12, 12, make_status_icon(status))

    # Cursor
    save_png("sprites/ui/cursor.png", 8, 12, make_cursor())

    # Save point crystal
    save_png("sprites/ui/save_point.png", 16, 16, make_save_point_crystal())

    # Treasure chests
    save_png("sprites/ui/chest_closed.png", 16, 14, make_treasure_chest(16, 14, False))
    save_png("sprites/ui/chest_open.png", 16, 14, make_treasure_chest(16, 14, True))

    # Portrait frame
    save_png("sprites/ui/portrait_frame.png", 32, 32, make_portrait_frame(32))

    # Coin/Gil icon
    coin = [TRANSPARENT] * (10 * 10)
    for y in range(10):
        for x in range(10):
            if (x-5)**2 + (y-5)**2 < 18:
                coin[y*10+x] = (220, 180, 40, 255)
            if (x-5)**2 + (y-5)**2 < 8:
                coin[y*10+x] = (240, 220, 80, 255)
    save_png("sprites/ui/coin.png", 10, 10, coin)

    # ===== OVERWORLD ICONS =====
    print("\n[Overworld Icons]")
    icon_types = ["town", "city", "dungeon", "forest", "desert", "mountain", "army_camp", "warren", "dragon_lair"]
    for icon_type in icon_types:
        save_png(f"sprites/ui/icon_{icon_type}.png", 16, 16, make_overworld_icon(icon_type))

    # ===== SPELL EFFECT ANIMATIONS =====
    print("\n[Spell/Ability Animations]")
    elements = ["fire", "ice", "thunder", "light", "darkness", "earth", "psychic", "heal", "water"]
    for element in elements:
        save_png(f"animations/spell_{element}.png", 16, 16, make_spell_effect(element))

    # Burn status indicator (small flame)
    burn_icon = make_spell_effect("fire", 12)
    save_png("animations/status_burn_indicator.png", 12, 12,
             [c if c != TRANSPARENT else (0,0,0,0) for c in burn_icon[:144]])

    # Bubble effect
    bubble = [TRANSPARENT] * (20 * 20)
    for y in range(20):
        for x in range(20):
            d = math.sqrt((x-10)**2 + (y-10)**2)
            if abs(d - 8) < 1.5:
                bubble[y*20+x] = (80, 180, 220, 180)
            elif abs(d - 7) < 0.8:
                bubble[y*20+x] = (120, 200, 240, 100)
    save_png("animations/spell_bubble.png", 20, 20, bubble)

    # Panda transform flash
    panda_flash = solid(16, 24, (240, 240, 240, 255))
    for y in range(24):
        for x in range(16):
            if (x < 3 or x > 12 or y > 20) and not (4 < x < 12 and 4 < y < 16):
                panda_flash[y*16+x] = (0,0,0,0)
    save_png("animations/panda_transform.png", 16, 24, panda_flash)

    # Skeleton summon (bone rising)
    skeleton_summon = [TRANSPARENT] * (16 * 24)
    bone_color = SKELETON_BONE
    for y in range(20, 24):
        for x in range(4, 12):
            skeleton_summon[y*16+x] = bone_color
    for y in range(12, 20):
        for x in range(6, 10):
            skeleton_summon[y*16+x] = bone_color
    save_png("animations/skeleton_summon.png", 16, 24, skeleton_summon)

    # Hannah scream flash (full-screen)
    hannah_flash = solid(256, 224, (255, 255, 255, 200))
    save_png("animations/hannah_scream_flash.png", 256, 224, hannah_flash)

    # Hannah ultimate spell explosion
    explosion = [TRANSPARENT] * (64 * 64)
    for y in range(64):
        for x in range(64):
            d = math.sqrt((x-32)**2 + (y-32)**2)
            if d < 30:
                intensity = max(0, 1.0 - d/30)
                r = min(255, int(255 * intensity))
                g = min(255, int(220 * intensity))
                b = min(255, int(200 * intensity))
                explosion[y*64+x] = (r, g, b, int(255 * intensity))
    save_png("animations/hannah_ultimate_explosion.png", 64, 64, explosion)

    # ===== PLACEHOLDER AUDIO NOTICE =====
    print("\n[Audio]")
    print("  ! Audio files (.ogg/.wav) must be sourced separately.")
    print("  ! Use royalty-free audio or generate with Godot's AudioStreamGenerator.")
    print("  ! Required tracks listed in project.godot and audio_manager.gd")

    # Write a placeholder .txt for audio directory
    os.makedirs("audio/music", exist_ok=True)
    os.makedirs("audio/sfx", exist_ok=True)
    with open("audio/AUDIO_REQUIRED.txt", "w") as f:
        f.write("""AUDIO FILES REQUIRED
====================
All audio must be royalty-free or original compositions.

MUSIC (.ogg format):
- title_theme.ogg
- overworld.ogg
- battle.ogg
- battle_kobold_heavy.ogg
- boss_battle.ogg
- final_boss.ogg
- town.ogg
- desert.ogg
- dungeon.ogg
- catacomb.ogg
- sad_theme.ogg (Flood death scene)
- victory.ogg
- game_over.ogg
- ending_good.ogg
- ending_best.ogg
- new_game_plus.ogg

SFX (.wav format):
- menu_select.wav, menu_confirm.wav, menu_cancel.wav
- battle_hit_physical.wav, battle_hit_magical.wav, battle_miss.wav
- spell_fire.wav, spell_ice.wav, spell_thunder.wav, spell_heal.wav, spell_psychic.wav
- status_burn_tick.wav, bubble_pop.wav
- level_up.wav, key_item_get.wav, treasure_chest.wav
- save_point.wav, door_open.wav, character_join.wav
- flood_death_impact.wav
- hannah_scream.wav (needs: pitch shift UP, distortion, reverb, echo)
- iris_berserk_roar.wav
- skeleton_summon.wav, panda_transform.wav
- hannah_ultimate_spell.wav

Recommended free sources:
- freesound.org (CC0 or CC-BY)
- OpenGameArt.org
- Godot's built-in AudioStreamGenerator for procedural SFX
""")
    print("  ✓ audio/AUDIO_REQUIRED.txt")

    print("\n" + "=" * 60)
    print("Asset generation complete!")
    print(f"Generated all sprite sheets, tilesets, backgrounds, UI elements.")
    print("Import into Godot with Texture Filter = Nearest for pixel-perfect rendering.")


if __name__ == "__main__":
    main()
