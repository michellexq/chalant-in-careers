"""
world_map.py – Draws the top-down world map with grass, path, and buildings.
Uses NumPy to generate the tile grid as a 2-D array.
"""

import numpy as np
import pygame
from constants import *


# Tile IDs
TILE_GRASS = 0
TILE_PATH  = 1


def build_tile_map() -> np.ndarray:
    """
    Returns a (MAP_ROWS, MAP_COLS) int array of tile IDs.
    A horizontal path runs through the middle rows.
    """
    grid = np.full((MAP_ROWS, MAP_COLS), TILE_GRASS, dtype=np.int8)
    # Horizontal path rows 8-11
    grid[8:12, :] = TILE_PATH
    # Vertical path from path to each building
    for col_centre in [6, 15, 24]:
        grid[5:9, col_centre-1:col_centre+2] = TILE_PATH
    return grid


class WorldMap:
    def __init__(self, tiles: dict):
        self.tiles    = tiles
        self.grid     = build_tile_map()
        self.px_w     = MAP_COLS * TILE
        self.px_h     = MAP_ROWS * TILE

        # Pre-render static map to a surface (faster than per-tile blitting every frame)
        self.surface  = pygame.Surface((self.px_w, self.px_h))
        self._bake()

    def _bake(self):
        for row in range(MAP_ROWS):
            for col in range(MAP_COLS):
                tid = self.grid[row, col]
                t = self.tiles["path"] if tid == TILE_PATH else self.tiles["grass"]
                self.surface.blit(t, (col * TILE, row * TILE))

    def draw(self, screen: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        screen.blit(self.surface, (-camera_x, -camera_y))

    def draw_buildings(self, screen: pygame.Surface, buildings: dict,
                       camera_x: int = 0, camera_y: int = 0):
        positions = {
            "clinic":      (ZONE_CLINIC[0]     * TILE, ZONE_CLINIC[1]     * TILE),
            "hotel":       (ZONE_HOTEL[0]      * TILE, ZONE_HOTEL[1]      * TILE),
            "realestate":  (ZONE_REALESTATE[0] * TILE, ZONE_REALESTATE[1] * TILE),
        }
        for key, (wx, wy) in positions.items():
            screen.blit(buildings[key], (wx - camera_x, wy - camera_y))
