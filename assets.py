"""
assets.py – Procedurally generated pixel-art sprites using NumPy + pygame.surfarray.
No external image files required; everything is drawn with NumPy arrays.
"""

import numpy as np
import pygame
from constants import *


# ── helpers ───────────────────────────────────────────────────────────────────

def _make_surface(arr: np.ndarray) -> pygame.Surface:
    """Convert an (H, W, 3) uint8 numpy array to a pygame Surface."""
    # Ensure C-contiguous layout required by frombuffer
    arr_c = np.ascontiguousarray(arr)
    return pygame.image.frombuffer(arr_c.tobytes(), (arr_c.shape[1], arr_c.shape[0]), "RGB")


def _make_surface_alpha(arr: np.ndarray) -> pygame.Surface:
    """Convert an (H, W, 4) uint8 numpy array to a per-pixel-alpha Surface."""
    arr_c = np.ascontiguousarray(arr)
    return pygame.image.frombuffer(arr_c.tobytes(), (arr_c.shape[1], arr_c.shape[0]), "RGBA").convert_alpha()


def _canvas(h, w, colour=(0, 0, 0, 0)):
    """Blank RGBA canvas."""
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[:, :] = colour
    return arr


def _rect(arr, r1, c1, r2, c2, colour):
    arr[r1:r2, c1:c2] = colour


# ── Player sprite (4 directions × 2 frames) ───────────────────────────────────

_PLAYER_W, _PLAYER_H = 24, 32

def _draw_player_frame(facing: str, foot: int) -> pygame.Surface:
    """
    facing: 'down','up','left','right'
    foot  : 0 or 1 (walk cycle)
    Returns a 24×32 RGBA surface.
    """
    a = _canvas(_PLAYER_H, _PLAYER_W)
    skin  = (255, 200, 150, 255)
    hair  = ( 60,  40,  20, 255)
    shirt = ( 80, 130, 200, 255)
    pants = ( 50,  80, 140, 255)
    shoe  = ( 40,  30,  20, 255)
    eye   = ( 30,  20,  10, 255)

    # head 8×8
    _rect(a,  0,  8, 8, 16, skin)
    _rect(a,  0,  8, 3, 16, hair)

    # eyes (facing-dependent)
    if facing == "down":
        a[5, 10] = eye; a[5, 13] = eye
    elif facing == "up":
        pass  # back of head – no eyes visible
    elif facing == "left":
        a[5,  8] = eye
    else:  # right
        a[5, 15] = eye

    # body 10×8
    _rect(a,  8,  8, 18, 16, shirt)

    # arms
    if foot == 0:
        _rect(a,  8,  5, 16,  8, shirt)
        _rect(a,  8, 16, 16, 19, shirt)
    else:
        _rect(a,  9,  5, 17,  8, shirt)
        _rect(a,  9, 16, 17, 19, shirt)

    # legs
    if foot == 0:
        _rect(a, 18,  8, 28, 12, pants)
        _rect(a, 18, 12, 28, 16, pants)
        _rect(a, 28,  8, 32, 12, shoe)
        _rect(a, 28, 12, 32, 16, shoe)
    else:
        _rect(a, 18,  9, 28, 13, pants)
        _rect(a, 18, 11, 28, 15, pants)
        _rect(a, 28,  9, 32, 13, shoe)
        _rect(a, 28, 11, 32, 15, shoe)

    return _make_surface_alpha(a)


def build_player_frames() -> dict:
    frames = {}
    for facing in ("down", "up", "left", "right"):
        frames[facing] = [_draw_player_frame(facing, 0),
                          _draw_player_frame(facing, 1)]
    return frames


# ── Building sprites ──────────────────────────────────────────────────────────

def _building(roof_col, wall_col, sign_col, label: str, w=5*TILE, h=4*TILE) -> pygame.Surface:
    a = _canvas(h, w)

    # wall
    _rect(a, h//3, 0, h, w, (*wall_col, 255))

    # roof (triangle approximation with rects)
    peak_row = 2
    for row in range(h // 3):
        slope = int(row * (w / 2) / (h // 3))
        _rect(a, row, slope, row+1, w - slope, (*roof_col, 255))

    # door
    dw, dh = 20, 30
    dc = w // 2 - dw // 2
    _rect(a, h - dh, dc, h, dc + dw, (60, 40, 20, 255))
    # door knob
    a[h - dh//2, dc + dw - 5] = (200, 160, 50, 255)

    # windows (2)
    for wx in [w//4 - 10, 3*w//4 - 10]:
        _rect(a, h//3 + 20, wx, h//3 + 50, wx + 25, (150, 210, 240, 255))
        # window cross
        a[h//3 + 35, wx:wx+25] = (80, 80, 100, 255)
        a[h//3+20:h//3+50, wx+12] = (80, 80, 100, 255)

    # sign above door
    _rect(a, h//3 + 5, w//2 - 35, h//3 + 22, w//2 + 35, (*sign_col, 255))

    return _make_surface_alpha(a)


def build_buildings() -> dict:
    return {
        "clinic":     _building((160, 60, 60),   (220, 200, 200), (200, 50, 50),  "CLINIC"),
        "hotel":      _building((60, 80, 180),    (200, 215, 240), (50, 80, 200),  "HOTEL"),
        "realestate": _building((50, 140, 60),    (200, 230, 205), (40, 160, 60),  "REALESTATE"),
    }


# ── Ground / grass tiles ──────────────────────────────────────────────────────

def build_tiles() -> dict:
    grass = np.full((TILE, TILE, 3), (85, 165, 75), dtype=np.uint8)
    # add some noise for texture
    rng = np.random.default_rng(42)
    noise = rng.integers(-15, 15, grass.shape, dtype=np.int16)
    grass = np.clip(grass.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    path = np.full((TILE, TILE, 3), (175, 155, 115), dtype=np.uint8)
    noise2 = rng.integers(-10, 10, path.shape, dtype=np.int16)
    path = np.clip(path.astype(np.int16) + noise2, 0, 255).astype(np.uint8)

    return {
        "grass": _make_surface(grass),
        "path":  _make_surface(path),
    }


# ── HUD coins icon ────────────────────────────────────────────────────────────

def build_coin_icon(size=20) -> pygame.Surface:
    a = _canvas(size, size)
    cx, cy, r = size//2, size//2, size//2 - 1
    for y in range(size):
        for x in range(size):
            if (x-cx)**2 + (y-cy)**2 <= r**2:
                a[y, x] = (245, 197, 24, 255)
            if (x-cx)**2 + (y-cy)**2 <= (r-3)**2:
                a[y, x] = (200, 150, 10, 255)
    return _make_surface_alpha(a)


# ── Entry arrow (animated hint over building door) ───────────────────────────

def build_arrow(colour=(245, 197, 24)) -> pygame.Surface:
    a = _canvas(20, 16)
    pts = [(0,0),(15,0),(7,19)]   # triangle pointing down
    for y in range(20):
        for x in range(16):
            # simple fill: check if inside triangle
            def sign(p1, p2, p3):
                return (p1[0]-p3[0])*(p2[1]-p3[1]) - (p2[0]-p3[0])*(p1[1]-p3[1])
            d1 = sign((x,y), pts[0], pts[1])
            d2 = sign((x,y), pts[1], pts[2])
            d3 = sign((x,y), pts[2], pts[0])
            has_neg = (d1<0) or (d2<0) or (d3<0)
            has_pos = (d1>0) or (d2>0) or (d3>0)
            if not (has_neg and has_pos):
                a[y, x] = (*colour, 255)
    return _make_surface_alpha(a)