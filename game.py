"""
game.py – Central state machine. Owns all scene instances and routes events.
"""

import pygame
from constants import *
from assets import (build_player_frames, build_buildings, build_tiles,
                    build_coin_icon, build_arrow)
from player import Player
from world_map import WorldMap
from scenes import (IntroScene, WorldScene, CareerScene,
                    ClinicChoiceScene, RealEstateChoiceScene)


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        # ── Build shared assets once ──────────────────────────────────────────
        self.player_frames = build_player_frames()
        self.buildings     = build_buildings()
        self.tiles         = build_tiles()
        self.coin_icon     = build_coin_icon()
        self.arrow         = build_arrow()

        # ── Game state ────────────────────────────────────────────────────────
        self.player_name = "Hero"
        self.gender      = "boy"
        self.coins       = 0

        # ── World objects (created once, reused across visits) ────────────────
        self.world_map   = WorldMap(self.tiles)
        self.player      = Player(
            self.player_frames,
            start_x = 15 * TILE,
            start_y = 9  * TILE
        )

        # ── Scene ─────────────────────────────────────────────────────────────
        self.current_scene = IntroScene(self.screen)

    # ── event routing ─────────────────────────────────────────────────────────
    def handle_event(self, event: pygame.event.Event):
        result = self.current_scene.handle_event(event)
        if result:
            self._transition(result)

    # ── update ────────────────────────────────────────────────────────────────
    def update(self, dt: float):
        self.current_scene.update(dt)

    # ── draw ──────────────────────────────────────────────────────────────────
    def draw(self):
        self.current_scene.draw()

    # ── transitions ───────────────────────────────────────────────────────────
    def _transition(self, result):
        """
        result: (action_str, payload_dict)
        """
        action, payload = result

        if action == "world":
            self.player_name = payload.get("player_name", "Hero")
            self.gender      = payload.get("gender", "boy")
            self.coins       = payload.get("coins", 0)
            self._go_world()

        elif action == "enter_building":
            building = payload["building"]
            if building == "clinic":
                self.current_scene = ClinicChoiceScene(self.screen, self.player_name)
            elif building == "hotel":
                from dialogue import HOTEL_SCRIPT
                self.current_scene = CareerScene(
                    self.screen, HOTEL_SCRIPT, self.player_name, self.coins)
            elif building == "realestate":
                self.current_scene = RealEstateChoiceScene(self.screen, self.player_name)

        elif action == "start_career":
            script      = payload["script"]
            house_index = payload.get("house_index", 0)
            self.current_scene = CareerScene(
                self.screen, script, self.player_name, self.coins,
                house_index=house_index)

        elif action == "back_to_world":
            earned = payload.get("earned", 0)
            self.coins += earned
            self._go_world()

    def _go_world(self):
        self.current_scene = WorldScene(
            screen      = self.screen,
            world_map   = self.world_map,
            buildings   = self.buildings,
            player      = self.player,
            player_name = self.player_name,
            coins       = self.coins,
        )
        self.current_scene.arrow_surf = self.arrow
