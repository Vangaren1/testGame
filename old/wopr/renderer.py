# renderer.py
import pygame
from .config import (
    W,
    H,
    GREEN,
    BLACK,
    USE_GLOW,
    USE_SCANLINES,
    USE_VIGNETTE,
    TOP_MARGIN,
    BOTTOM_MARGIN,
    LEFT_MARGIN,
)
from .effects import draw_scanlines


def draw_terminal(screen, font, st, vignette=None):
    # 1) Render terminal content to an offscreen surface
    term = pygame.Surface((W, H))
    term.fill(BLACK)

    y = TOP_MARGIN
    line_height = font.get_linesize()
    usable_height = H - TOP_MARGIN - BOTTOM_MARGIN
    max_lines = max(1, usable_height // line_height)

    for line in st.lines[-max_lines:]:
        term.blit(font.render(line, True, GREEN), (LEFT_MARGIN, y))
        y += line_height

    # Blinking cursor
    cursor_on = int((st.blink * 2) % 2) == 0  # ~1Hz blink (on/off 0.5s each)
    prompt_text = font.render(st.prompt + st.buffer, True, GREEN)
    term.blit(prompt_text, (LEFT_MARGIN, y))
    if cursor_on:
        cx = prompt_text.get_width()
        pygame.draw.rect(term, GREEN, (LEFT_MARGIN + cx + 6, y + 4, 12, 18))

    # 2) Optional glow pass
    frame = term
    if USE_GLOW:
        glow = pygame.transform.smoothscale(term, (int(W * 1.02), int(H * 1.02)))
        frame = pygame.transform.smoothscale(glow, (W, H))

    # 3) Blit to screen
    screen.blit(frame, (0, 0))

    # 4) Overlays
    if USE_SCANLINES:
        draw_scanlines(screen)
    if USE_VIGNETTE and vignette:
        screen.blit(vignette, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    pygame.display.flip()
