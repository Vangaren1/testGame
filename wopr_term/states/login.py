
# states/login.py
import pygame
from ..engine import State
from .prompt import PromptState

class LoginState(State):
    def enter(self):
        self.username = None
        self.term.prompt = "LOGON> "
        self.term.println("REMOTE TERMINAL ACCESS")
        self.term.println()

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.engine.quit()
            elif e.type == pygame.TEXTINPUT:
                self.term.handle_textinput(e.text)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.engine.quit()
                else:
                    entry = self.term.handle_keydown(e.key)
                    if entry is not None:
                        txt = entry.strip()
                        self.term.println(self.term.prompt + txt)
                        if self.username is None:
                            self.username = txt
                            self.term.prompt = "PASSWORD> "
                        else:
                            if (self.username or "").lower() == "joshua":
                                self.term.println("ACCESS GRANTED")
                                self.engine.set_state(PromptState)
                                return
                            else:
                                self.term.println("ACCESS DENIED")
                                self.username = None
                                self.term.prompt = "LOGON> "

    def update(self, dt):
        self.term.blink += dt
