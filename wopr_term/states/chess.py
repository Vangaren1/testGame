
# states/chess.py
import pygame
from ..engine import State
# Hook up python-chess later if desired

class ChessState(State):
    def enter(self):
        self.term.prompt = "CHESS> "
        self.term.println("CHESS MODE READY.")
        self.term.println("CMDS: BOARD, MOVE <...>, UNDO, RESET, EXIT (back)")

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.engine.quit()
            elif e.type == pygame.TEXTINPUT:
                self.term.handle_textinput(e.text)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    from .prompt import PromptState
                    self.engine.set_state(PromptState)
                else:
                    entry = self.term.handle_keydown(e.key)
                    if entry is not None:
                        cmd = entry.strip().upper()
                        self.term.println(self.term.prompt + cmd)
                        if cmd == "EXIT":
                            from .prompt import PromptState
                            self.engine.set_state(PromptState)
                        elif cmd == "BOARD":
                            self.term.println("[board here]")
                        elif cmd.startswith("MOVE"):
                            self.term.println("OK.")
                        elif cmd == "RESET":
                            self.term.println("NEW GAME.")
                        elif cmd == "UNDO":
                            self.term.println("TAKEN BACK.")
                        else:
                            self.term.println("UNKNOWN CHESS CMD.")

    def update(self, dt):
        self.term.blink += dt
