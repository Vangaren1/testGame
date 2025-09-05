# state.py
from dataclasses import dataclass, field
from typing import List


@dataclass
class TerminalState:
    lines: List[str] = field(default_factory=list)
    buffer: str = ""
    prompt: str = "LOGON> "
    running: bool = True
    blink: float = 0.0  # seconds accumulator
