import sys
import pygame
import time
import random

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from level import Level
from player import Player
from enemigo import Enemy
from renderer import render
from fisicas_gpu import GPUPhysics

MAP_FILE = "mapa.csv"
MOUSE_SENSITIVITY = 0.12
USE_GPU = True
NUM_ENEMIES = 3000
USE_RANDOM_MAP = True
MAP_WIDTH = 100
MAP_HEIGHT = 100
WALL_PROBABILITY = 0.15

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
    gluPerspective(75, width / height, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

    game_map = Level()
    if USE_RANDOM_MAP:
        game_map.generate(MAP_WIDTH,MAP_HEIGHT,WALL_PROBABILITY)
    else:
        game_map.load(MAP_FILE)

    player = Player(game_map.player_spawn[0],game_map.player_spawn[1])

    free_positions = []

    for y, row in enumerate(game_map.grid):
        for x, cell in enumerate(row):
            if cell == 0:
                free_positions.append((x + 0.5, y + 0.5))

    enemies = []

    for _ in range(NUM_ENEMIES):
        x, y = random.choice(free_positions)
        enemies.append(Enemy(x, y))

    items = []
    particles = []

    gpu_physics = None

    if USE_GPU:
        gpu_physics = GPUPhysics()

    clock = pygame.time.Clock()
    last_print = time.time()

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
                player.pitch = max(-90, min(90, player.pitch))

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("BANG!")

        keys = pygame.key.get_pressed()

        player.update(dt, keys, game_map)

        start = time.perf_counter()

        if USE_GPU:
            gpu_physics.update_entities_gpu(
                enemies,
                items,
                particles,
                player,
                game_map,
                dt
            )
        else:
            for enemy in enemies:
                enemy.update(player, game_map, dt)

        elapsed = (time.perf_counter() - start) * 1000

        render(
            game_map,
            player,
            enemies,
            items,
            particles
        )

        pygame.display.flip()

        current = time.time()

        if current - last_print >= 1:
            mode = "GPU" if USE_GPU else "CPU"

            print(
                f"{mode} | "
                f"Enemigos: {NUM_ENEMIES} | "
                f"FPS: {clock.get_fps():.2f} | "
                f"Actualización: {elapsed:.4f} ms"
            )

            last_print = current


if __name__ == "__main__":
    main()