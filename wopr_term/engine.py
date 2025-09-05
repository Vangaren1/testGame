
# engine.py
import pygame
from .terminal import Terminal
from .effects import make_vignette
from .config import W, H, FONT_NAME, FONT_SIZE, USE_VIGNETTE

class State:
    def __init__(self, engine):
        self.engine = engine
        self.term = engine.term

    def enter(self):
        pass

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        self.term.draw(screen, self.engine.vignette)

class Engine:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.term = Terminal(font)
        self.vignette = make_vignette((W, H)) if USE_VIGNETTE else None
        self.running = True
        self.state = None

    def set_state(self, state_cls, *args, **kwargs):
        self.state = state_cls(self, *args, **kwargs)
        self.state.enter()

    def quit(self):
        self.running = False
