
# main.py
import pygame
from .config import W, H, FONT_NAME, FONT_SIZE
from .engine import Engine
from .states.login import LoginState

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE) or pygame.font.Font(None, FONT_SIZE)

    engine = Engine(screen, font)
    engine.set_state(LoginState)

    pygame.key.start_text_input()

    while engine.running:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()

        # advance blink
        engine.term.blink += dt

        # state cycle
        engine.state.handle_events(events)
        engine.state.update(dt)
        engine.state.draw(screen)

    pygame.quit()

if __name__ == "__main__":
    main()
