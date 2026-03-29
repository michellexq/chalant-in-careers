"""
player.py – Movable character with 4-directional animation.
Movement uses NumPy for velocity normalisation.
"""

import numpy as np
import pygame
from constants import *


class Player:
    def __init__(self, frames: dict, start_x: float, start_y: float):
        self.frames   = frames          # dict: facing -> [surf0, surf1]
        self.x        = float(start_x)
        self.y        = float(start_y)
        self.facing   = "down"
        self.foot     = 0               # animation frame index
        self.anim_t   = 0.0             # accumulator for walk cycle
        self.anim_spd = 0.18            # seconds per step

        self.w = frames["down"][0].get_width()
        self.h = frames["down"][0].get_height()

    # ── rect for collision ────────────────────────────────────────────────────
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    @property
    def feet_rect(self) -> pygame.Rect:
        """Smaller rect at feet level for tile/zone detection."""
        return pygame.Rect(int(self.x) + 6, int(self.y) + self.h - 8, self.w - 12, 8)

    # ── update ────────────────────────────────────────────────────────────────
    def update(self, dt: float, keys, world_rect: pygame.Rect):
        # Build velocity vector using NumPy
        vx, vy = 0.0, 0.0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: vx = -1.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: vx =  1.0
        if keys[pygame.K_UP]    or keys[pygame.K_w]: vy = -1.0
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: vy =  1.0

        vel = np.array([vx, vy], dtype=np.float64)
        mag = np.linalg.norm(vel)
        if mag > 0:
            vel = vel / mag          # normalise → diagonal = same speed as cardinal
            vel *= PLAYER_SPEED * dt

            # Update facing
            if abs(vel[0]) >= abs(vel[1]):
                self.facing = "right" if vel[0] > 0 else "left"
            else:
                self.facing = "down" if vel[1] > 0 else "up"

            # Walk animation
            self.anim_t += dt
            if self.anim_t >= self.anim_spd:
                self.anim_t -= self.anim_spd
                self.foot = 1 - self.foot
        else:
            self.foot = 0
            self.anim_t = 0.0

        # Apply movement, clamped to world bounds
        new_x = self.x + vel[0]
        new_y = self.y + vel[1]
        self.x = float(np.clip(new_x, world_rect.left, world_rect.right  - self.w))
        self.y = float(np.clip(new_y, world_rect.top,  world_rect.bottom - self.h))

    # ── draw ──────────────────────────────────────────────────────────────────
    def draw(self, surface: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        surf = self.frames[self.facing][self.foot]
        surface.blit(surf, (int(self.x) - camera_x, int(self.y) - camera_y))

    # ── check if inside a tile zone ───────────────────────────────────────────
    def in_zone(self, zone_tile_rect) -> bool:
        """zone_tile_rect is (col, row, w_tiles, h_tiles)."""
        col, row, wt, ht = zone_tile_rect
        zone_px = pygame.Rect(col*TILE, row*TILE, wt*TILE, ht*TILE)
        return zone_px.colliderect(self.feet_rect)
