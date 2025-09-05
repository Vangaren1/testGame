# input_handler.py
import pygame
from .state import TerminalState


def noop(*args, **kwargs):
    pass


def handle_events(st: TerminalState) -> None:
    for event in pygame.event.get():
        handler = FUNC_MAP.get(getattr(event, "type", None), noop)
        handler(st, event)


def on_quit(st: TerminalState, event: pygame.event.Event):
    st.running = False


def on_text_input(st: TerminalState, event: pygame.event.Event):
    # TEXTINPUT carries composed text (handles IME, dead keys, etc.)
    if event.text not in "\r\n\t":
        st.buffer += event.text


def on_keydown(st: TerminalState, event: pygame.event.Event):
    handler = KEY_MAP.get(event.key, noop)
    handler(st, event)


def on_escape(st: TerminalState, event: pygame.event.Event):
    st.running = False


def on_enter(st: TerminalState, event: pygame.event.Event):
    cmd = st.buffer.strip().upper()
    st.lines.append(st.prompt + st.buffer)
    st.buffer = ""
    if cmd == "HELP":
        st.lines.append("CMDS: HELP, STATUS, HACK, CLEAR, EXIT")
    elif cmd == "STATUS":
        st.lines.append("SYS STATUS: NOMINAL  NET: ONLINE  TEMP: 32C")
    elif cmd == "CLEAR":
        st.lines.clear()
    elif cmd in ("EXIT", "QUIT"):
        st.running = False
    elif cmd:
        st.lines.append(f"UNKNOWN CMD: {cmd}")


def on_backspace(st: TerminalState, event: pygame.event.Event):
    st.buffer = st.buffer[:-1]


# Maps
FUNC_MAP = {
    pygame.QUIT: on_quit,
    pygame.TEXTINPUT: on_text_input,
    pygame.KEYDOWN: on_keydown,
}

KEY_MAP = {
    pygame.K_ESCAPE: on_escape,
    pygame.K_RETURN: on_enter,
    pygame.K_KP_ENTER: on_enter,
    pygame.K_BACKSPACE: on_backspace,
}
