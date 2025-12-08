import csv
import pygame
import random

from visual_objects import SongGalaxy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BG_COLOR = (5, 5, 20)
PATH = "spotify_songs.csv"
MAX_ROWS = 50


# AI-GENERATED SECTION 1
def load_data(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows
# END AI-GENERATED SECTION 1


def main():
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont(None, 18)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Spotify Song Galaxy")
    clock = pygame.time.Clock()

    rows = load_data(PATH)
    if len(rows) > MAX_ROWS:
        random.shuffle(rows)
        rows = rows[:MAX_ROWS]

    center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen_radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 2 - 10

    galaxy = SongGalaxy(rows, center, screen_radius)

    running = True
    mouse_pos = center

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos


            # AI-GENERATED SECTION 2
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    galaxy.zoom *= 1.12 ** event.y
                else:
                    galaxy.zoom *= 0.88 ** abs(event.y)

                # keep zoom within limits
                galaxy.zoom = max(galaxy.min_zoom,
                                  min(galaxy.max_zoom, galaxy.zoom))
            # END AI-GENERATED SECTION 2


            elif event.type == pygame.KEYDOWN:

                # AI-GENERATED SECTION 3
                if event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                    galaxy.zoom = min(galaxy.max_zoom, galaxy.zoom * 1.12)

                elif event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE):
                    galaxy.zoom = max(galaxy.min_zoom, galaxy.zoom * 0.88)
                # END AI-GENERATED SECTION 3


        screen.fill(BG_COLOR)

        galaxy.update(dt)
        galaxy.display(screen, mouse_pos, font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


# Summary: Approximately 30% of the above code was generated or assisted by AI.