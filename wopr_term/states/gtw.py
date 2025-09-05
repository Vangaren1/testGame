
# states/gtw.py
import pygame
from ..engine import State

class GTWState(State):
    def enter(self):
        self.term.prompt = "GTW> "
        self.term.println("SELECT SIDE: USA / USSR")
        self.term.println("HINT: TYPE 'USA' OR 'USSR'")
        self.t0 = 0.0
        self.defcon = 5

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
                        if cmd in ("USA", "USSR"):
                            self.term.println(f"SIDE CONFIRMED: {cmd}")
                            self.term.println("INITIALIZING STRATEGIC MODEL...")
                        elif cmd == "EXIT":
                            from .prompt import PromptState
                            self.engine.set_state(PromptState)
                        else:
                            self.term.println("ACK.")

    def update(self, dt):
        self.term.blink += dt
        self.t0 += dt
        new_defcon = max(1, 5 - int(self.t0 // 6))
        if new_defcon != self.defcon:
            self.defcon = new_defcon
            self.term.println(f"DEFCON STATUS: {self.defcon}")
        if self.defcon == 1:
            self.term.println("SIMULATION COMPLETE.")
            self.term.println("A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.")
            from .prompt import PromptState
            self.engine.set_state(PromptState)
