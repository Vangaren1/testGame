"""
wopr_term/states/tictactoe.py
Basic Tic-Tac-Toe state: verifies layout only.
- Top 3/4: board area (colored)
- Bottom 1/4: terminal area (colored)
"""

import pygame

# --- robust import so this file can run directly OR via package ---
try:
    # Normal package usage (python -m wopr_term.states.tictactoe)
    from ..engine import State
except ImportError:
    # Direct-run fallback: add project root to sys.path and import absolute
    import os, sys

    _HERE = os.path.dirname(__file__)
    _ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
    if _ROOT not in sys.path:
        sys.path.insert(0, _ROOT)
    from wopr_term.engine import State  # type: ignore

# --- colors for visual debugging ---
GREEN = (0, 255, 120)
BLACK = (0, 0, 0)

# --- colors for visual debugging ---
BOARD_BG = (30, 50, 90)  # not black
TERM_BG = (20, 20, 20)
SEP_COL = (90, 90, 90)


class TicTacToeState(State):
    """
    Minimal layout/debug version.
    Draws only two rectangles and a separator line.
    """

    def enter(self):
        # 👇 borrow the engine’s terminal so self.term exists
        if not hasattr(self, "term") or self.term is None:
            self.term = getattr(self.engine, "term", None)

        self._recompute_layout(self.engine.screen.get_size())

        # game state
        self.board = [[" "] * 3 for _ in range(3)]
        self.turn = "X"
        self.sel = [1, 1]

        # initialize the terminal UI
        if self.term is not None:
            self.term.clear()
            self.term.prompt = "TIC-TAC-TOE> "
            self.term.println("Arrows=move  Enter/Space=place  Esc=back")
        else:
            # helpful one-time debug
            print("⚠️ No engine terminal attached; bottom pane will remain blank.")

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.engine.quit()
            elif e.type == pygame.VIDEORESIZE:
                # Recompute rectangles on window resize
                self._recompute_layout((e.w, e.h))
            elif e.type == pygame.TEXTINPUT and hasattr(self, "term") and self.term:
                self.term.handle_textinput(e.text)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    try:
                        from .prompt import PromptState

                        self.engine.set_state(PromptState)
                    except Exception:
                        self.engine.quit()
                elif e.key in (pygame.K_LEFT, pygame.K_a):
                    self.sel[1] = max(0, self.sel[1] - 1)
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    self.sel[1] = min(2, self.sel[1] + 1)
                elif e.key in (pygame.K_UP, pygame.K_w):
                    self.sel[0] = max(0, self.sel[0] - 1)
                elif e.key in (pygame.K_DOWN, pygame.K_s):
                    self.sel[0] = min(2, self.sel[0] + 1)
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    r, c = self.sel
                    if self.board[r][c] == " ":
                        self.board[r][c] = self.turn
                        self.turn = "O" if self.turn == "X" else "X"

    def draw(self, surface):
        # 1) backgrounds
        self.render(surface)

        # 2) board grid + selection + marks
        bx, by, bw, bh = self.board_rect
        cs = bw // 3
        grid_col = (230, 230, 230)
        sel_col = (90, 180, 250)

        for i in (1, 2):
            x = bx + i * cs
            y = by + i * cs
            pygame.draw.line(surface, grid_col, (x, by), (x, by + bh), 2)
            pygame.draw.line(surface, grid_col, (bx, y), (bx + bw, y), 2)

        r, c = self.sel
        sel_rect = pygame.Rect(bx + c * cs, by + r * cs, cs, cs).inflate(-6, -6)
        pygame.draw.rect(surface, sel_col, sel_rect, 3)

        pad = max(8, cs // 8)
        for rr in range(3):
            for cc in range(3):
                mark = self.board[rr][cc]
                cell = pygame.Rect(bx + cc * cs, by + rr * cs, cs, cs).inflate(
                    -pad, -pad
                )
                if mark == "X":
                    pygame.draw.line(
                        surface, (220, 80, 80), cell.topleft, cell.bottomright, 6
                    )
                    pygame.draw.line(
                        surface, (220, 80, 80), cell.topright, cell.bottomleft, 6
                    )
                elif mark == "O":
                    center = cell.center
                    radius = min(cell.w, cell.h) // 2
                    pygame.draw.circle(surface, (80, 200, 220), center, radius, 6)

        # 3) terminal in bottom quarter
        if hasattr(self, "term") and hasattr(self.term, "render"):
            term_view = surface.subsurface(self.term_rect)
            self.term.render(term_view)

    def render(self, surface):
        # ensure layout
        if not hasattr(self, "top_rect") or not hasattr(self, "term_rect"):
            self._recompute_layout(surface.get_size())

        # backgrounds
        surface.fill(BOARD_BG, self.top_rect)
        surface.fill(TERM_BG, self.term_rect)

        # separator
        pygame.draw.line(
            surface,
            SEP_COL,
            (self.term_rect.left, self.term_rect.top),
            (self.term_rect.right, self.term_rect.top),
            2,
        )

        # OPTIONAL: comment out labels entirely while testing
        # (labels don't affect fill, but let's remove variables)
        # -- no labels here --

    # ----- layout helpers -----
    def _recompute_layout(self, size):
        W, H = size
        top_h = int(H * 0.75)

        print(f"top_h: {top_h}, H: {H}, H - top_h: {H - top_h}")

        # Two main areas
        self.top_rect = pygame.Rect(0, 0, W, top_h)  # top 3/4
        self.term_rect = pygame.Rect(0, top_h, W, H - top_h)  # bottom 1/4

        # Centered square board inside the top area (just for visual guide)
        side = min(self.top_rect.w, self.top_rect.h)
        bx = self.top_rect.x + (self.top_rect.w - side) // 2
        by = self.top_rect.y + (self.top_rect.h - side) // 2
        self.board_rect = pygame.Rect(bx, by, side, side)

        # (Optional) precompute 3x3 cells for later
        cs = side // 3
        self.cell_rects = [
            [pygame.Rect(bx + c * cs, by + r * cs, cs, cs) for c in range(3)]
            for r in range(3)
        ]


# --- Optional: allow running this file directly during development ---
if __name__ == "__main__":
    """
    Direct-run debug mode.
    Preferred: `python -m wopr_term.states.tictactoe`
    This fallback tries to use a dev runner if available, else spins a tiny loop.
    """
    try:
        # Try your reusable runner if you created wopr_term/dev_runner.py
        from wopr_term.dev_runner import run_state  # type: ignore

        run_state(
            TicTacToeState, window_size=(1000, 700), caption="TicTacToe — Layout Debug"
        )
    except Exception:
        # Minimal inline loop if dev_runner is not present
        class _MiniEngine:
            def __init__(self, size=(1000, 700)):
                pygame.init()
                self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                pygame.display.set_caption("TicTacToe — Layout Debug (inline)")
                self.clock = pygame.time.Clock()
                self.running = True
                self.state = TicTacToeState(self)
                self.state.enter()

            def quit(self):
                self.running = False

            def loop(self):
                while self.running:
                    events = pygame.event.get()
                    self.state.handle_events(events)
                    self.screen.fill((0, 0, 0))
                    self.state.render(self.screen)
                    pygame.display.flip()
                    self.clock.tick(60)
                pygame.quit()

        _MiniEngine().loop()
