# main.py
import pygame
from .config import W, H, FONT_NAME, FONT_SIZE, USE_VIGNETTE
from .state import TerminalState
from .effects import make_vignette
from .input_handler import handle_events
from .renderer import draw_terminal


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    # robust font load
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    if not font:
        font = pygame.font.Font(None, FONT_SIZE)

    vignette = make_vignette((W, H)) if USE_VIGNETTE else None
    st = TerminalState()

    # Helps TEXTINPUT on some platforms
    pygame.key.start_text_input()

    while st.running:
        dt = clock.tick(60) / 1000.0
        st.blink += dt

        handle_events(st)
        draw_terminal(screen, font, st, vignette)

    pygame.quit()


if __name__ == "__main__":
    main()
