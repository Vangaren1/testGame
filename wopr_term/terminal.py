# terminal.py
import pygame
from .config import (
    W,
    H,
    GREEN,
    BLACK,
    TOP_MARGIN,
    BOTTOM_MARGIN,
    LEFT_MARGIN,
    USE_GLOW,
    USE_SCANLINES,
    USE_VIGNETTE,
)
from .effects import draw_scanlines


class Terminal:
    def __init__(self, font):
        self.font = font
        self.lines = []
        self.buffer = ""
        self.prompt = "LOGON> "
        self.blink = 0.0

    # output
    def println(self, text=""):
        self.lines.append(text)

    def clear(self):
        self.lines.clear()

    # input helpers
    def handle_textinput(self, txt):
        if txt not in "\r\n\t":
            self.buffer += txt

    def handle_keydown(self, key):
        if key == pygame.K_BACKSPACE:
            self.buffer = self.buffer[:-1]
            return None
        if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            cmdline = self.buffer
            self.buffer = ""
            return cmdline
        return None

    # drawing
    def draw(self, screen, vignette=None):
        term = pygame.Surface((W, H))
        term.fill(BLACK)

        y = TOP_MARGIN
        lh = self.font.get_linesize()
        usable = H - TOP_MARGIN - BOTTOM_MARGIN
        max_lines = max(1, usable // lh)

        for line in self.lines[-max_lines:]:
            term.blit(self.font.render(line, True, GREEN), (LEFT_MARGIN, y))
            y += lh

        prompt_text = self.font.render(self.prompt + self.buffer, True, GREEN)
        term.blit(prompt_text, (LEFT_MARGIN, y))
        cursor_on = int((self.blink * 2) % 2) == 0  # ~1Hz
        if cursor_on:
            cx = prompt_text.get_width()
            pygame.draw.rect(term, GREEN, (LEFT_MARGIN + cx + 6, y + 4, 12, 18))

        frame = term
        if USE_GLOW:
            glow = pygame.transform.smoothscale(term, (int(W * 1.02), int(H * 1.02)))
            frame = pygame.transform.smoothscale(glow, (W, H))

        screen.blit(frame, (0, 0))
        if USE_SCANLINES:
            draw_scanlines(screen)
        if USE_VIGNETTE and vignette:
            screen.blit(vignette, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        pygame.display.flip()

    # terminal.py
    def render(self, surface):
        # surface is already clipped to just the terminal area
        surface.fill((0, 0, 0))  # or transparent bg if you want
        # draw all lines, prompt, cursor starting at (0,0) in this surface
