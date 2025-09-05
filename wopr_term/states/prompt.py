
# states/prompt.py
import pygame
from ..engine import State
from .chess import ChessState
from .gtw import GTWState

class PromptState(State):
    def enter(self):
        self.term.prompt = "> "
        self.term.println()
        self.term.println("WOPR SYSTEM 4.0  (c) 1983")
        self.term.println("TYPE HELP FOR COMMANDS.")

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
                        cmd = entry.strip().upper()
                        self.term.println(self.term.prompt + cmd)
                        self.route_command(cmd)

    def route_command(self, cmd):
        if not cmd:
            return
        if cmd == "HELP":
            self.term.println("CMDS: HELP, STATUS, GAMES, PLAY <NAME>, CLEAR, EXIT")
        elif cmd == "STATUS":
            self.term.println("SYS STATUS: NOMINAL  NET: ONLINE  TEMP: 32C")
        elif cmd == "CLEAR":
            self.term.clear()
        elif cmd == "EXIT":
            self.engine.quit()
        elif cmd == "GAMES":
            for g in [
                "FALKEN'S MAZE","BLACK JACK","GIN RUMMY","HEARTS","CHESS",
                "POKER","FIGHTER COMBAT","GUERRILLA ENGAGEMENT","DESERT WARFARE",
                "AIR-TO-GROUND ACTIONS","THEATERWIDE TACTICAL WARFARE","GLOBAL THERMONUCLEAR WAR"
            ]:
                self.term.println(g)
        elif cmd.startswith("PLAY"):
            name = cmd[4:].strip()
            if name == "CHESS":
                self.engine.set_state(ChessState)
            elif name == "GLOBAL THERMONUCLEAR WAR":
                self.engine.set_state(GTWState)
            else:
                self.term.println(f"{name or '(none)'}: (demo not implemented)")
        else:
            self.term.println("UNKNOWN COMMAND. TYPE HELP.")

    def update(self, dt):
        self.term.blink += dt
