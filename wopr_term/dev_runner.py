# dev_runner.py
import pygame
from typing import Optional, Type


class MiniTerminal:
    """Minimal terminal that matches the methods your state expects:
    - clear(), println(), handle_textinput(text), handle_keydown(key) -> Optional[str]
    - render(surface), and a 'prompt' attribute.
    """

    def __init__(self, font_name=None, font_size=18):
        pygame.font.init()
        self.font = pygame.font.SysFont(font_name, font_size)
        self.lines = []
        self.buffer = ""
        self.prompt = "> "

    def clear(self):
        self.lines.clear()
        self.buffer = ""

    def println(self, s: str):
        self.lines.append(s)

    def handle_textinput(self, text: str):
        self.buffer += text

    def handle_keydown(self, key: int) -> Optional[str]:
        if key == pygame.K_BACKSPACE:
            if self.buffer:
                self.buffer = self.buffer[:-1]
            return None
        if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            entry = self.buffer
            self.buffer = ""
            return entry
        return None  # regular chars come via TEXTINPUT

    def render(self, surface: pygame.Surface):
        # Draw inside the provided subsurface (origin is 0,0 here)
        surface.fill((10, 10, 10))
        pad = 8
        color = (220, 220, 220)
        w, h = surface.get_size()
        line_h = self.font.get_linesize()

        # Show as many lines as fit (minus 1 row for prompt)
        max_rows = max(1, (h - pad * 2) // line_h - 1)
        tail = self.lines[-max_rows:] if self.lines else []

        y = pad
        for s in tail:
            # simple truncation (keep it minimal)
            surf = self.font.render(s, True, color)
            surface.blit(surf, (pad, y))
            y += line_h

        # Blink cursor
        blink_on = (pygame.time.get_ticks() // 500) % 2 == 0
        cursor = "_" if blink_on else " "
        prompt_str = f"{self.prompt}{self.buffer}{cursor}"
        surface.blit(self.font.render(prompt_str, True, color), (pad, h - pad - line_h))


class MiniEngine:
    """Small engine: window, loop, and state switching."""

    def __init__(self, size=(1000, 700), caption="State Runner", bg=(0, 0, 0)):
        pygame.init()
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.running = True
        self.bg = bg
        self.state = None

    def set_state(self, StateCls: Type):
        self.state = StateCls(self)
        if hasattr(self.state, "enter"):
            self.state.enter()

    def quit(self):
        self.running = False

    def loop(self):
        while self.running:
            events = pygame.event.get()
            if self.state and hasattr(self.state, "handle_events"):
                self.state.handle_events(events)

            self.screen.fill(self.bg)
            if self.state and hasattr(self.state, "render"):
                self.state.render(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


def run_state(StateCls: Type, *, window_size=(1000, 700), caption="State Runner"):
    """Boot a given State class (expects __init__(engine), enter(), handle_events(), render())."""
    eng = MiniEngine(size=window_size, caption=caption)
    # If the state needs a terminal and hasn't created one yet, attach a minimal one:
    if not hasattr(StateCls, "_dev_runner_injected"):
        orig_enter = getattr(StateCls, "enter", None)

        def patched_enter(self):
            # Ensure self.term exists
            if not hasattr(self, "term") or self.term is None:
                self.term = MiniTerminal()
            # Ensure layout exists
            if not hasattr(self, "_recompute_layout"):

                def _recompute_layout(size):
                    W, H = size
                    top_h = int(H * 0.75)
                    self.top_rect = pygame.Rect(0, 0, W, top_h)
                    self.term_rect = pygame.Rect(0, top_h, W, H - top_h)
                    side = min(self.top_rect.w, self.top_rect.h)
                    bx = self.top_rect.x + (self.top_rect.w - side) // 2
                    by = self.top_rect.y + (self.top_rect.h - side) // 2
                    self.board_rect = pygame.Rect(bx, by, side, side)
                    cs = side // 3
                    self.cell_rects = [
                        [
                            pygame.Rect(bx + c * cs, by + r * cs, cs, cs)
                            for c in range(3)
                        ]
                        for r in range(3)
                    ]

                self._recompute_layout = _recompute_layout
            self._recompute_layout(self.engine.screen.get_size())

            # Call user's enter if present
            if callable(orig_enter):
                orig_enter(self)

        StateCls.enter = patched_enter

        # Ensure resize handled
        orig_handle = getattr(StateCls, "handle_events", None)

        def patched_handle(self, events):
            for e in events:
                if e.type == pygame.VIDEORESIZE:
                    self._recompute_layout((e.w, e.h))
            if callable(orig_handle):
                orig_handle(self, events)

        StateCls.handle_events = patched_handle

        # Provide a default render if the state doesn’t define one
        if not hasattr(StateCls, "render"):

            def default_render(self, surface: pygame.Surface):
                BOARD_BG = (18, 18, 18)
                TERM_BG = (10, 10, 10)
                if not hasattr(self, "top_rect") or not hasattr(self, "term_rect"):
                    self._recompute_layout(surface.get_size())
                surface.fill(BOARD_BG, self.top_rect)

                # If user has a board drawer, call it
                if hasattr(self, "_draw_board"):
                    self._draw_board(surface)

                surface.fill(TERM_BG, self.term_rect)
                pygame.draw.line(
                    surface,
                    (80, 80, 80),
                    (self.term_rect.left, self.term_rect.top),
                    (self.term_rect.right, self.term_rect.top),
                    1,
                )
                term_view = surface.subsurface(self.term_rect)
                if hasattr(self.term, "render"):
                    self.term.render(term_view)

            StateCls.render = default_render

        # Mark so we don’t re-patch on subsequent runs
        StateCls._dev_runner_injected = True

    eng.set_state(StateCls)
    eng.loop()
