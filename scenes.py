"""
scenes.py – One class per scene. The Game object swaps between them.
"""

import pygame
import numpy as np
from constants import *
from ui import (FontCache, Button, TypewriterText, InputBox,
                draw_panel, draw_text, draw_wrapped_text, wrap_text)
from dialogue import (CLINIC_DOCTOR, CLINIC_PSYCH, HOTEL_SCRIPT,
                      REALESTATE_SCRIPTS, get_score_rating, get_feedback)


# ─────────────────────────────────────────────────────────────────────────────
# IntroScene  (name entry + character select)
# ─────────────────────────────────────────────────────────────────────────────

class IntroScene:
    def __init__(self, screen):
        self.screen  = screen
        W, H         = SCREEN_W, SCREEN_H
        self.title_y = -80     # animate in
        self.alpha   = 0

        self.input   = InputBox(pygame.Rect(W//2 - 160, H//2 + 20, 320, 40),
                                placeholder="Enter your name…")
        self.confirm = Button(pygame.Rect(W//2 - 80, H//2 + 80, 160, 44),
                              "Start  ▶", colour=(60, 140, 80))
        self.gender  = "boy"
        self.btn_boy  = Button(pygame.Rect(W//2 - 130, H//2 - 40, 110, 36),
                               "👦 Boy",  colour=(60, 100, 180))
        self.btn_girl = Button(pygame.Rect(W//2 + 20,  H//2 - 40, 110, 36),
                               "👧 Girl", colour=(180, 80, 140))
        self.error   = ""

        # Starfield using numpy
        rng = np.random.default_rng(7)
        self.stars = rng.integers(0, [SCREEN_W, SCREEN_H], size=(120, 2))
        self.star_bright = rng.random(120)

    def handle_event(self, event):
        result = self.input.handle_event(event)
        if result:
            return self._try_confirm(result)
        if self.confirm.handle_event(event):
            return self._try_confirm(self.input.text.strip())
        if self.btn_boy.handle_event(event):
            self.gender = "boy"
        if self.btn_girl.handle_event(event):
            self.gender = "girl"
        return None

    def _try_confirm(self, name):
        if not name:
            self.error = "Please enter a name first!"
            return None
        return ("world", {"player_name": name, "gender": self.gender, "coins": 0})

    def update(self, dt):
        self.title_y = min(60, self.title_y + 200 * dt)
        self.alpha   = min(255, self.alpha + 300 * dt)
        self.input.update(dt)

    def draw(self):
        s = self.screen
        s.fill(C_BG)

        # Stars
        for i, (sx, sy) in enumerate(self.stars):
            b = int(self.star_bright[i] * 200 + 55)
            s.set_at((sx, sy), (b, b, b))

        W, H = SCREEN_W, SCREEN_H

        # Title
        font_big  = FontCache.get(38, bold=True)
        font_med  = FontCache.get(18)
        font_sm   = FontCache.get(14)

        title = font_big.render("CareerQuest", True, C_BORDER)
        s.blit(title, (W//2 - title.get_width()//2, int(self.title_y)))

        sub = font_sm.render("Discover your calling. Master your role.", True, C_TEXT_DIM)
        s.blit(sub, (W//2 - sub.get_width()//2, int(self.title_y) + 50))

        # Panel
        panel_rect = pygame.Rect(W//2 - 200, H//2 - 90, 400, 240)
        draw_panel(s, panel_rect)

        label = font_med.render("Who are you?", True, C_TEXT)
        s.blit(label, (W//2 - label.get_width()//2, H//2 - 80))

        self.btn_boy.draw(s)
        self.btn_girl.draw(s)

        sel_label = font_sm.render(f"Selected: {self.gender.capitalize()}", True, C_YELLOW)
        s.blit(sel_label, (W//2 - sel_label.get_width()//2, H//2 - 5))

        self.input.draw(s)
        self.confirm.draw(s)

        if self.error:
            err = font_sm.render(self.error, True, C_RED)
            s.blit(err, (W//2 - err.get_width()//2, H//2 + 132))


# ─────────────────────────────────────────────────────────────────────────────
# WorldScene  (top-down map with movable character)
# ─────────────────────────────────────────────────────────────────────────────

class WorldScene:
    def __init__(self, screen, world_map, buildings, player, player_name, coins):
        self.screen      = screen
        self.world_map   = world_map
        self.buildings   = buildings
        self.player      = player
        self.player_name = player_name
        self.coins       = coins

        self.world_rect = pygame.Rect(0, 0, MAP_COLS * TILE, MAP_ROWS * TILE)
        self.camera_x   = 0
        self.camera_y   = 0

        # Entrance prompts
        self.near_zone   = None
        self.prompt_anim = 0.0
        self.arrow_surf  = None   # set from game

        # HUD fonts
        self.f_hud  = FontCache.get(15, bold=True)
        self.f_sm   = FontCache.get(13)
        self.f_hint = FontCache.get(14)

        # Zones info
        self.zones = {
            "clinic":     ZONE_CLINIC,
            "hotel":      ZONE_HOTEL,
            "realestate": ZONE_REALESTATE,
        }
        self.zone_labels = {
            "clinic":     "🏥 The Clinic",
            "hotel":      "🛋  The Hotel",
            "realestate": "🏡 The Avenue",
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_e, pygame.K_RETURN):
            if self.near_zone:
                return ("enter_building", {"building": self.near_zone})
        return None

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.world_rect)

        # Camera follow
        cx = int(self.player.x) - SCREEN_W // 2 + self.player.w // 2
        cy = int(self.player.y) - SCREEN_H // 2 + self.player.h // 2
        self.camera_x = max(0, min(cx, self.world_rect.w - SCREEN_W))
        self.camera_y = max(0, min(cy, self.world_rect.h - SCREEN_H))

        # Zone proximity
        self.near_zone = None
        for name, zone in self.zones.items():
            if self.player.in_zone(zone):
                self.near_zone = name
                break

        self.prompt_anim += dt * 3

    def draw(self):
        s = self.screen
        s.fill((30, 80, 30))

        self.world_map.draw(s, self.camera_x, self.camera_y)
        self.world_map.draw_buildings(s, self.buildings, self.camera_x, self.camera_y)
        self.player.draw(s, self.camera_x, self.camera_y)

        # Zone labels above buildings
        for name, zone in self.zones.items():
            bx = zone[0] * TILE - self.camera_x + zone[2] * TILE // 2
            by = zone[1] * TILE - self.camera_y - 20
            label = self.zone_labels[name]
            lsurf = self.f_sm.render(label, True, C_YELLOW)
            s.blit(lsurf, (bx - lsurf.get_width()//2, by))

        # Entry prompt
        if self.near_zone:
            offset = int(np.sin(self.prompt_anim) * 4)
            prompt = self.f_hint.render("Press [E] or [Enter] to enter", True, C_WHITE)
            px = SCREEN_W // 2 - prompt.get_width() // 2
            py = SCREEN_H - 80 + offset
            draw_panel(s, pygame.Rect(px - 12, py - 8, prompt.get_width() + 24, prompt.get_height() + 16))
            s.blit(prompt, (px, py))

        # HUD (top bar)
        hud_rect = pygame.Rect(0, 0, SCREEN_W, 36)
        draw_panel(s, hud_rect, bg=(10, 10, 25, 200), border=(60, 60, 100), radius=0)
        name_s = self.f_hud.render(f"  {self.player_name}", True, C_TEXT)
        s.blit(name_s, (8, 8))
        coin_s = self.f_hud.render(f"💰 {self.coins} coins", True, C_YELLOW)
        s.blit(coin_s, (SCREEN_W - coin_s.get_width() - 16, 8))
        ctrl = self.f_sm.render("WASD / Arrow keys to move", True, C_TEXT_DIM)
        s.blit(ctrl, (SCREEN_W//2 - ctrl.get_width()//2, 10))


# ─────────────────────────────────────────────────────────────────────────────
# CareerScene  (chat-based conversation)
# ─────────────────────────────────────────────────────────────────────────────

class CareerScene:
    """Shared conversation engine for all three career buildings."""

    def __init__(self, screen, script: dict, player_name: str, coins: int,
                 house_index: int = 0):
        self.screen      = screen
        self.script      = script
        self.player_name = player_name
        self.coins       = coins

        self.turn        = 0          # current dialogue turn
        self.score       = 0
        self.max_score   = len(script["turns"]) * 2   # max 2 pts per turn

        # Replace {name} placeholder
        intro_raw = script["intro"].replace("{name}", player_name)
        self.typewriter  = TypewriterText(intro_raw, speed=50)
        self.phase       = "intro"    # intro → npc → choice → result
        self.npc_tw      = None
        self.choice_btns = []
        self.feedback_tw = None
        self.end_btn     = None
        self.result_data = None

        # Chat log  [(speaker, text), ...]
        self.chat_log    = []
        self.scroll_y    = 0

        self.f_title = FontCache.get(17, bold=True)
        self.f_body  = FontCache.get(14)
        self.f_sm    = FontCache.get(13)
        self.f_npc   = FontCache.get(14)

        self._build_end_session_btn()

    # ── layout constants ─────────────────────────────────────────────────────
    CHAT_X   = 20
    CHAT_Y   = 80
    CHAT_W   = 580
    CHAT_H   = 380
    RIGHT_X  = 620
    RIGHT_W  = 320

    def _build_end_session_btn(self):
        self.end_btn = Button(
            pygame.Rect(self.RIGHT_X, SCREEN_H - 56, self.RIGHT_W, 40),
            "End Session  ⏹",
            colour=(140, 50, 50)
        )

    def _build_choice_buttons(self):
        self.choice_btns = []
        choices = self.script["turns"][self.turn]["choices"]
        for i, (text, pts) in enumerate(choices):
            btn = Button(
                pygame.Rect(self.RIGHT_X,
                            100 + i * 88,
                            self.RIGHT_W, 78),
                text,
                colour=(40, 60, 110),
                font_size=12
            )
            btn._pts = pts
            self.choice_btns.append(btn)

    def _start_npc_turn(self):
        npc_text = self.script["turns"][self.turn]["npc"]
        self.npc_tw = TypewriterText(npc_text, speed=45)
        self.phase  = "npc"
        self.choice_btns = []

    def _advance_to_choices(self):
        self.phase = "choice"
        self._build_choice_buttons()
        npc_text = self.script["turns"][self.turn]["npc"]
        self.chat_log.append((self.script["npc_name"], npc_text))

    def _player_chose(self, choice_text: str, pts: int):
        self.score += pts
        self.chat_log.append((self.player_name, choice_text))
        self.turn += 1
        if self.turn >= len(self.script["turns"]):
            self._end_session()
        else:
            self._start_npc_turn()

    def _end_session(self):
        self.phase = "result"
        label, wage, col = get_score_rating(self.score, self.max_score)
        fb = get_feedback(self.score, self.max_score, self.script["role"])
        self.result_data = {
            "label": label, "wage": wage, "col": col,
            "feedback": fb,
            "score": self.score, "max": self.max_score,
        }

    # ── events ────────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if self.phase == "intro":
            if event.type == pygame.KEYDOWN or (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                if not self.typewriter.done:
                    self.typewriter.skip()
                else:
                    self._start_npc_turn()

        elif self.phase == "npc":
            if event.type == pygame.KEYDOWN or (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                if not self.npc_tw.done:
                    self.npc_tw.skip()
                else:
                    self._advance_to_choices()

        elif self.phase == "choice":
            for btn in self.choice_btns:
                if btn.handle_event(event):
                    self._player_chose(btn.text, btn._pts)
                    break
            if self.end_btn and self.end_btn.handle_event(event):
                self._end_session()

        elif self.phase == "result":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return ("back_to_world", {"earned": self.result_data["wage"]})
            # back button
            if hasattr(self, "_back_btn") and self._back_btn.handle_event(event):
                return ("back_to_world", {"earned": self.result_data["wage"]})

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.phase != "result":
                return ("back_to_world", {"earned": 0})
        return None

    # ── update ────────────────────────────────────────────────────────────────
    def update(self, dt):
        if self.phase == "intro":
            self.typewriter.update(dt)
        elif self.phase == "npc" and self.npc_tw:
            self.npc_tw.update(dt)

    # ── draw ─────────────────────────────────────────────────────────────────
    def draw(self):
        s = self.screen
        s.fill(C_BG)

        W, H = SCREEN_W, SCREEN_H

        # Header bar
        draw_panel(s, pygame.Rect(0, 0, W, 68), bg=(10, 10, 30, 240), radius=0)
        role_s = self.f_title.render(self.script["role"], True, C_BORDER)
        s.blit(role_s, (16, 10))
        set_s = self.f_sm.render(self.script["setting"], True, C_TEXT_DIM)
        s.blit(set_s, (16, 36))
        ctx_s = self.f_sm.render(self.script["context"], True, C_BLUE)
        s.blit(ctx_s, (W//2 - ctx_s.get_width()//2, 50))

        turn_s = self.f_sm.render(f"Turn {self.turn}/{len(self.script['turns'])}   Score: {self.score}/{self.max_score}", True, C_TEXT_DIM)
        s.blit(turn_s, (W - turn_s.get_width() - 16, 10))

        if self.phase in ("choice", "npc", "intro"):
            self._draw_chat(s)
            self._draw_right_panel(s)
        elif self.phase == "result":
            self._draw_result(s)

    def _draw_chat(self, s):
        chat_rect = pygame.Rect(self.CHAT_X, self.CHAT_Y, self.CHAT_W, self.CHAT_H)
        draw_panel(s, chat_rect)

        # Scrollable chat log
        y = self.CHAT_Y + 10
        line_h = 20
        max_w  = self.CHAT_W - 24
        f = self.f_sm

        for speaker, text in self.chat_log[-14:]:
            is_player = (speaker == self.player_name)
            col = C_GREEN if is_player else C_BLUE
            spk = f.render(f"{speaker}:", True, col)
            s.blit(spk, (self.CHAT_X + 10, y))
            y += spk.get_height() + 2
            for line in wrap_text(text, f, max_w - 10):
                ls = f.render(line, True, C_TEXT)
                s.blit(ls, (self.CHAT_X + 20, y))
                y += ls.get_height() + 2
            y += 6

        # Live typewriter text
        if self.phase == "intro" and self.typewriter:
            vis = self.typewriter.visible
            for line in wrap_text(vis, f, max_w - 10):
                ls = f.render(line, True, C_YELLOW)
                if y + ls.get_height() < self.CHAT_Y + self.CHAT_H - 10:
                    s.blit(ls, (self.CHAT_X + 10, y))
                    y += ls.get_height() + 3
            hint_col = C_TEXT_DIM if not self.typewriter.done else C_WHITE
            hint = f.render("Click or press any key to continue…", True, hint_col)
            s.blit(hint, (self.CHAT_X + 10, self.CHAT_Y + self.CHAT_H - 26))

        elif self.phase == "npc" and self.npc_tw:
            npc_label = self.f_sm.render(f"{self.script['npc_name']}:", True, C_BLUE)
            s.blit(npc_label, (self.CHAT_X + 10, y))
            y += npc_label.get_height() + 2
            for line in wrap_text(self.npc_tw.visible, f, max_w - 10):
                ls = f.render(line, True, C_TEXT)
                if y + ls.get_height() < self.CHAT_Y + self.CHAT_H - 10:
                    s.blit(ls, (self.CHAT_X + 20, y))
                    y += ls.get_height() + 3
            if self.npc_tw.done:
                hint = f.render("Click to choose your response…", True, C_TEXT_DIM)
                s.blit(hint, (self.CHAT_X + 10, self.CHAT_Y + self.CHAT_H - 26))

    def _draw_right_panel(self, s):
        # Right panel background
        draw_panel(s, pygame.Rect(self.RIGHT_X - 8, self.CHAT_Y,
                                  self.RIGHT_W + 8, SCREEN_H - self.CHAT_Y - 10))

        if self.phase == "choice":
            lbl = self.f_body.render("Your response:", True, C_BORDER)
            s.blit(lbl, (self.RIGHT_X, self.CHAT_Y + 12))
            for btn in self.choice_btns:
                btn.draw(s)
            # Hint
            hint = self.script["turns"][self.turn].get("hint", "")
            if hint:
                hint_r = pygame.Rect(self.RIGHT_X, 380, self.RIGHT_W, 60)
                draw_panel(s, hint_r, bg=(20, 40, 20, 200), border=(74, 222, 128))
                draw_wrapped_text(s, f"💡 {hint}", self.f_sm, C_GREEN, hint_r.inflate(-10, -10))
            self.end_btn.draw(s)
        elif self.phase in ("intro", "npc"):
            info = self.f_sm.render("💬 Conversation in progress", True, C_TEXT_DIM)
            s.blit(info, (self.RIGHT_X, self.CHAT_Y + 20))
            esc = self.f_sm.render("[ESC] Exit without pay", True, (160, 80, 80))
            s.blit(esc, (self.RIGHT_X, SCREEN_H - 70))

    def _draw_result(self, s):
        if not hasattr(self, "_back_btn"):
            self._back_btn = Button(
                pygame.Rect(SCREEN_W//2 - 120, SCREEN_H - 80, 240, 46),
                "Return to Map  🗺",
                colour=(50, 120, 60)
            )

        rd = self.result_data
        col_map = {"green": C_GREEN, "yellow": C_YELLOW, "red": C_RED}
        col = col_map.get(rd["col"], C_WHITE)

        # Central result panel
        panel = pygame.Rect(SCREEN_W//2 - 280, 80, 560, SCREEN_H - 180)
        draw_panel(s, panel)

        y = panel.y + 20
        title = self.f_title.render("Session Complete!", True, C_BORDER)
        s.blit(title, (SCREEN_W//2 - title.get_width()//2, y)); y += 40

        rating = FontCache.get(22, bold=True).render(rd["label"], True, col)
        s.blit(rating, (SCREEN_W//2 - rating.get_width()//2, y)); y += 46

        score_s = self.f_body.render(f"Score: {rd['score']} / {rd['max']}", True, C_TEXT)
        s.blit(score_s, (SCREEN_W//2 - score_s.get_width()//2, y)); y += 36

        wage_s = FontCache.get(18, bold=True).render(f"💰 Earned: {rd['wage']} coins", True, C_YELLOW)
        s.blit(wage_s, (SCREEN_W//2 - wage_s.get_width()//2, y)); y += 44

        fb_title = self.f_body.render("Feedback:", True, C_BORDER)
        s.blit(fb_title, (panel.x + 30, y)); y += 28

        for line in rd["feedback"]:
            fb_s = self.f_sm.render(f"  • {line}", True, C_TEXT)
            s.blit(fb_s, (panel.x + 30, y)); y += 26

        y += 10
        esc = self.f_sm.render("Press [Enter] or click below to return", True, C_TEXT_DIM)
        s.blit(esc, (SCREEN_W//2 - esc.get_width()//2, y))

        self._back_btn.draw(s)


# ─────────────────────────────────────────────────────────────────────────────
# ClinicChoiceScene  (doctor vs psychologist picker)
# ─────────────────────────────────────────────────────────────────────────────

class ClinicChoiceScene:
    def __init__(self, screen, player_name):
        self.screen      = screen
        self.player_name = player_name
        self.f_title = FontCache.get(22, bold=True)
        self.f_body  = FontCache.get(15)
        W, H = SCREEN_W, SCREEN_H
        self.btn_doc  = Button(pygame.Rect(W//2 - 220, H//2 + 20, 200, 54),
                               "🩺 Doctor",  colour=(60, 130, 190))
        self.btn_psy  = Button(pygame.Rect(W//2 + 20,  H//2 + 20, 200, 54),
                               "🧠 Psychologist", colour=(120, 60, 170))
        self.btn_back = Button(pygame.Rect(W//2 - 80,  H//2 + 100, 160, 40),
                               "← Back",    colour=(80, 80, 80))

    def handle_event(self, event):
        if self.btn_doc.handle_event(event):
            return ("start_career", {"script": CLINIC_DOCTOR})
        if self.btn_psy.handle_event(event):
            return ("start_career", {"script": CLINIC_PSYCH})
        if self.btn_back.handle_event(event):
            return ("back_to_world", {})
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return ("back_to_world", {})
        return None

    def update(self, dt): pass

    def draw(self):
        s = self.screen
        s.fill(C_BG)
        W, H = SCREEN_W, SCREEN_H
        draw_panel(s, pygame.Rect(W//2 - 300, H//2 - 120, 600, 280))
        title = self.f_title.render("🏥 The Clinic", True, C_BORDER)
        s.blit(title, (W//2 - title.get_width()//2, H//2 - 110))
        sub = self.f_body.render("Choose your role:", True, C_TEXT)
        s.blit(sub, (W//2 - sub.get_width()//2, H//2 - 60))
        desc_d = FontCache.get(12).render("Diagnose & treat physical ailments", True, C_TEXT_DIM)
        s.blit(desc_d, (W//2 - 220, H//2 + 80))
        desc_p = FontCache.get(12).render("Support mental wellbeing", True, C_TEXT_DIM)
        s.blit(desc_p, (W//2 + 20, H//2 + 80))
        self.btn_doc.draw(s)
        self.btn_psy.draw(s)
        self.btn_back.draw(s)


# ─────────────────────────────────────────────────────────────────────────────
# RealEstateChoiceScene  (pick house 1, 2, or 3)
# ─────────────────────────────────────────────────────────────────────────────

class RealEstateChoiceScene:
    def __init__(self, screen, player_name):
        self.screen      = screen
        self.player_name = player_name
        self.f_title = FontCache.get(20, bold=True)
        self.f_body  = FontCache.get(14)
        W, H = SCREEN_W, SCREEN_H
        labels = ["🏠 House 1\nStarter Cottage\n$480k",
                  "🏡 House 2\nFamily Home\n$720k",
                  "🏰 House 3\nLuxury Estate\n$1.45M"]
        self.btns = []
        for i in range(3):
            self.btns.append(Button(
                pygame.Rect(W//2 - 310 + i * 210, H//2 + 10, 190, 60),
                labels[i].split("\n")[0],
                colour=(50, 100, 60)
            ))
        self.btn_back = Button(pygame.Rect(W//2 - 80, H//2 + 100, 160, 40),
                               "← Back", colour=(80, 80, 80))
        self.descs = [s.split("\n")[1:] for s in labels]

    def handle_event(self, event):
        for i, btn in enumerate(self.btns):
            if btn.handle_event(event):
                return ("start_career", {"script": REALESTATE_SCRIPTS[i], "house_index": i})
        if self.btn_back.handle_event(event):
            return ("back_to_world", {})
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return ("back_to_world", {})
        return None

    def update(self, dt): pass

    def draw(self):
        s = self.screen
        s.fill(C_BG)
        W, H = SCREEN_W, SCREEN_H
        draw_panel(s, pygame.Rect(W//2 - 330, H//2 - 120, 660, 280))
        title = self.f_title.render("🏡 The Avenue – Choose a Property", True, C_BORDER)
        s.blit(title, (W//2 - title.get_width()//2, H//2 - 110))
        for i, btn in enumerate(self.btns):
            btn.draw(s)
            for j, line in enumerate(self.descs[i]):
                dl = FontCache.get(12).render(line, True, C_TEXT_DIM)
                s.blit(dl, (W//2 - 310 + i * 210, H//2 + 76 + j * 16))
        self.btn_back.draw(s)
