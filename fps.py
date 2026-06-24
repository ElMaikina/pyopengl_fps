import sys
import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from level import Level
from player import Player
from enemigo import Enemy
from renderer import render

MAP_FILE = "mapa.csv"
MOUSE_SENSITIVITY = 0.12


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (0, 0),
        OPENGL | DOUBLEBUF | FULLSCREEN
    )

    width, height = screen.get_size()

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(
        75,
        width / height,
        0.1,
        100.0
    )

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

    game_map = Level()
    game_map.load(MAP_FILE)

    player = Player(
        game_map.player_spawn[0],
        game_map.player_spawn[1]
    )

    enemies = [
    Enemy(5.5, 1.5),
    Enemy(6.5, 2.5),
    Enemy(1.5, 3.5)
]

    items = []
    particles = []

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(144) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEMOTION:
                dx, dy = event.rel

                player.yaw -= dx * MOUSE_SENSITIVITY
                player.pitch += dy * MOUSE_SENSITIVITY

                player.pitch = max(
                    -90,
                    min(90, player.pitch)
                )

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("BANG!")

        keys = pygame.key.get_pressed()

        player.update(
            dt,
            keys,
            game_map
        )

        for enemy in enemies:
            enemy.update(
                player,
                game_map,
                dt
            )

        render(
            game_map,
            player,
            enemies,
            items,
            particles
        )

        pygame.display.flip()


if __name__ == "__main__":
    main()