import pygame

WIDTH, HEIGHT = 800, 600
BG = (18, 18, 18)
FG = (230, 230, 230)
ACCENT = (90, 180, 230)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rect keyboard demo (no mouse)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    # Our rectangle: x, y, w, h
    rect = pygame.Rect(100, 100, 160, 100)

    speed_px = 6
    inflate_px = 6
    running = True

    while running:
        # --- events (NO MOUSE NEEDED) ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                # snap helpers (edges)
                elif e.key == pygame.K_r:  # snap left to 0
                    rect.left = 0
                elif e.key == pygame.K_f:  # snap right to WIDTH
                    rect.right = WIDTH
                elif e.key == pygame.K_t:  # snap top to 0
                    rect.top = 0
                elif e.key == pygame.K_g:  # snap bottom to HEIGHT
                    rect.bottom = HEIGHT
                # center helpers
                elif e.key == pygame.K_c:
                    rect.center = (WIDTH // 2, HEIGHT // 2)
                # resize (inflate keeps center unless edges are constrained by later clamps)
                elif e.key == pygame.K_RIGHTBRACKET:  # ]
                    rect.inflate_ip(inflate_px, inflate_px)
                elif e.key == pygame.K_LEFTBRACKET:  # [
                    rect.inflate_ip(-inflate_px, -inflate_px)

        # continuous key presses for smooth movement
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed_px
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speed_px
        if dx or dy:
            rect.move_ip(dx, dy)

        # keep rect fully on screen
        if rect.w < 1:
            rect.w = 1
        if rect.h < 1:
            rect.h = 1
        rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        # --- draw ---
        screen.fill(BG)

        # draw the rect (filled) and an outline
        pygame.draw.rect(screen, ACCENT, rect)
        pygame.draw.rect(screen, FG, rect, width=2)

        # crosshair at center
        cx, cy = rect.center
        pygame.draw.line(screen, FG, (cx - 10, cy), (cx + 10, cy), 1)
        pygame.draw.line(screen, FG, (cx, cy - 10), (cx, cy + 10), 1)

        # text panel
        lines = [
            "Controls: Arrow keys move | [ / ] shrink/grow | R/F/T/G snap edges | C center | Q/ESC quit",
            f"rect: x={rect.x} y={rect.y} w={rect.w} h={rect.h}",
            f"edges: left={rect.left} right={rect.right} top={rect.top} bottom={rect.bottom}",
            f"center: {rect.center} | size: {rect.size}",
            f"topleft={rect.topleft} topright={rect.topright} bottomleft={rect.bottomleft} bottomright={rect.bottomright}",
        ]
        y = 10
        for s in lines:
            surf = font.render(s, True, FG)
            screen.blit(surf, (10, y))
            y += surf.get_height() + 4

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
