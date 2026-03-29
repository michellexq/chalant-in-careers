"""
ui.py – Reusable UI helpers: text wrapping, panels, buttons, typewriter effect.
"""

import pygame
from constants import *


class FontCache:
    _fonts: dict = {}

    @classmethod
    def get(cls, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in cls._fonts:
            try:
                cls._fonts[key] = pygame.font.SysFont("monospace", size, bold=bold)
            except Exception:
                cls._fonts[key] = pygame.font.Font(None, size)
        return cls._fonts[key]


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_panel(surface: pygame.Surface, rect: pygame.Rect,
               bg=(15, 15, 35, 220), border=C_BORDER, radius=8):
    """Draw a rounded semi-transparent panel."""
    panel = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 0))
    pygame.draw.rect(panel, bg, panel.get_rect(), border_radius=radius)
    pygame.draw.rect(panel, (*border, 255), panel.get_rect(), width=2, border_radius=radius)
    surface.blit(panel, (rect.x, rect.y))


def draw_text(surface, text, font, colour, x, y):
    surf = font.render(text, True, colour)
    surface.blit(surf, (x, y))
    return surf.get_height()


def draw_wrapped_text(surface, text, font, colour, rect: pygame.Rect, line_spacing=4):
    """Draw wrapped text inside a rect; returns total height used."""
    lines = wrap_text(text, font, rect.w)
    y = rect.y
    for line in lines:
        surf = font.render(line, True, colour)
        surface.blit(surf, (rect.x, y))
        y += surf.get_height() + line_spacing
    return y - rect.y


class Button:
    def __init__(self, rect: pygame.Rect, text: str,
                 colour=C_BORDER, text_colour=C_BLACK, font_size=16):
        self.rect       = rect
        self.text       = text
        self.colour     = colour
        self.hover_col  = tuple(min(255, c + 40) for c in colour)
        self.text_colour = text_colour
        self.font_size  = font_size
        self._hovered   = False

    def handle_event(self, event) -> bool:
        """Returns True if this button was clicked."""
        if event.type == pygame.MOUSEMOTION:
            self._hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface: pygame.Surface):
        col = self.hover_col if self._hovered else self.colour
        pygame.draw.rect(surface, col, self.rect, border_radius=6)
        pygame.draw.rect(surface, C_WHITE, self.rect, width=2, border_radius=6)
        font = FontCache.get(self.font_size)
        text_surf = font.render(self.text, True, self.text_colour)
        tx = self.rect.x + (self.rect.w - text_surf.get_width()) // 2
        ty = self.rect.y + (self.rect.h - text_surf.get_height()) // 2
        surface.blit(text_surf, (tx, ty))


class TypewriterText:
    """Animates text appearing character-by-character."""
    def __init__(self, text: str, speed: float = 40.0):
        self.full_text  = text
        self.speed      = speed   # characters per second
        self.progress   = 0.0
        self.done       = False

    def update(self, dt: float):
        if not self.done:
            self.progress += self.speed * dt
            if self.progress >= len(self.full_text):
                self.progress = len(self.full_text)
                self.done = True

    def skip(self):
        self.progress = len(self.full_text)
        self.done = True

    @property
    def visible(self) -> str:
        return self.full_text[:int(self.progress)]


class InputBox:
    """Single-line text input widget."""
    def __init__(self, rect: pygame.Rect, placeholder="Type here…", font_size=16):
        self.rect        = rect
        self.placeholder = placeholder
        self.font_size   = font_size
        self.text        = ""
        self.active      = True
        self.cursor_t    = 0.0

    def handle_event(self, event) -> str | None:
        """Returns submitted text on RETURN, else None."""
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                val = self.text.strip()
                self.text = ""
                return val if val else None
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if event.unicode and len(self.text) < 60:
                    self.text += event.unicode
        return None

    def update(self, dt: float):
        self.cursor_t += dt

    def draw(self, surface: pygame.Surface):
        font = FontCache.get(self.font_size)
        pygame.draw.rect(surface, (30, 30, 55), self.rect, border_radius=5)
        pygame.draw.rect(surface, C_BORDER, self.rect, width=2, border_radius=5)
        display = self.text if self.text else self.placeholder
        colour  = C_WHITE if self.text else C_TEXT_DIM
        # cursor blink
        show_cursor = self.active and (int(self.cursor_t * 2) % 2 == 0)
        if show_cursor and self.text is not None:
            display = self.text + "|"
        text_surf = font.render(display, True, colour)
        surface.blit(text_surf, (self.rect.x + 8, self.rect.y + (self.rect.h - text_surf.get_height()) // 2))
