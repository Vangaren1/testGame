
# effects.py
import math
import pygame
from .config import W, H

def make_vignette(size):
    w, h = size
    surf = pygame.Surface(size, pygame.SRCALPHA)
    cx, cy = w // 2, h // 2
    max_r = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            r = math.hypot(x - cx, y - cy)
            k = int(255 - (165 * (r / max_r) ** 1.6))  # 255 → ~90 at edges
            surf.set_at((x, y), (k, k, k, 255))
    return surf

def draw_scanlines(target):
    for y in range(0, H, 2):
        pygame.draw.line(target, (0, 20, 0), (0, y), (W, y), 1)
