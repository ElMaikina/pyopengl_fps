import csv
import math
import sys
import numpy as np

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

MAP_FILE = "mapa.csv"

BLOCK_SIZE = 1.0
PLAYER_RADIUS = 0.25

ACCELERATION = 12.0
DECELERATION = 10.0
MAX_SPEED = 4.0

MOUSE_SENSITIVITY = 0.12

PLAYER_HEIGHT = 0.4

class MapData:
    def __init__(self):
        self.grid = []
        self.width = 0
        self.height = 0
        self.player_spawn = (1.5, 1.5)

    def load(self, filename):
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            self.grid = []
            last_player = None
            for y, row in enumerate(reader):
                parsed_row = []
                for x, value in enumerate(row):
                    try:
                        v = int(value)
                    except:
                        v = 0
                    if v == 2:
                        last_player = (x + 0.5, y + 0.5)
                        parsed_row.append(0)
                    elif v == 1:
                        parsed_row.append(1)
                    else:
                        parsed_row.append(0)
                self.grid.append(parsed_row)
        self.height = len(self.grid)
        self.width = max(len(r) for r in self.grid)
        if last_player is not None:
            self.player_spawn = last_player

    def is_wall(self, x, y):
        gx = int(x)
        gy = int(y)
        if gx < 0 or gy < 0:
            return True
        if gy >= self.height:
            return True
        if gx >= len(self.grid[gy]):
            return True
        return self.grid[gy][gx] == 1

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.yaw = 0.0
        self.pitch = 0.0
        self.h = PLAYER_HEIGHT

    def forward_vector(self):
        r = math.radians(self.yaw)
        return np.array([
            math.sin(r),
            math.cos(r)
        ], dtype=np.float32)

    def right_vector(self):
        r = math.radians(self.yaw)
        return np.array([
            math.cos(r),
            -math.sin(r)
        ], dtype=np.float32)

    def update(self, dt, keys, game_map):
        movement = np.array([0.0, 0.0], dtype=np.float32)
        if keys[K_w]:
            movement -= self.forward_vector()
        if keys[K_s]:
            movement += self.forward_vector()
        if keys[K_d]:
            movement += self.right_vector()
        if keys[K_a]:
            movement -= self.right_vector()
        length = np.linalg.norm(movement)
        if length > 0:
            movement /= length
            self.vx += movement[0] * ACCELERATION * dt
            self.vy += movement[1] * ACCELERATION * dt
        else:
            speed = math.hypot(self.vx, self.vy)
            if speed > 0:
                decel = DECELERATION * dt
                speed = max(0.0, speed - decel)
                if speed == 0:
                    self.vx = 0
                    self.vy = 0
                else:
                    factor = speed / math.hypot(self.vx, self.vy)
                    self.vx *= factor
                    self.vy *= factor
        speed = math.hypot(self.vx, self.vy)
        if speed > MAX_SPEED:
            factor = MAX_SPEED / speed
            self.vx *= factor
            self.vy *= factor
        self.move_with_collision(dt, game_map)

    def move_with_collision(self, dt, game_map):
        new_x = self.x + self.vx * dt
        if not collide_circle(
            new_x,
            self.y,
            PLAYER_RADIUS,
            game_map
        ):
            self.x = new_x
        new_y = self.y + self.vy * dt
        if not collide_circle(
            self.x,
            new_y,
            PLAYER_RADIUS,
            game_map
        ):
            self.y = new_y

def collide_circle(px, py, radius, game_map):
    min_x = int(px - radius)
    max_x = int(px + radius)
    min_y = int(py - radius)
    max_y = int(py + radius)
    for gy in range(min_y, max_y + 1):
        for gx in range(min_x, max_x + 1):
            if not game_map.is_wall(gx + 0.5, gy + 0.5):
                continue
            nearest_x = max(gx, min(px, gx + 1))
            nearest_y = max(gy, min(py, gy + 1))
            dx = px - nearest_x
            dy = py - nearest_y
            if dx * dx + dy * dy < radius * radius:
                return True
    return False

def draw_cube(x, y):
    glPushMatrix()
    glTranslatef(x + 0.5, 0.5, y + 0.5)
    glBegin(GL_QUADS)
    # TOP
    glColor3f(0.7, 0.7, 0.7)

    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    # BOTTOM
    glColor3f(0.3, 0.3, 0.3)

    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    # FRONT
    glColor3f(0.8, 0.2, 0.2)

    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    # BACK
    glColor3f(0.2, 0.8, 0.2)

    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    # LEFT
    glColor3f(0.2, 0.2, 0.8)

    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    # RIGHT
    glColor3f(0.8, 0.8, 0.2)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)

    glEnd()
    glPopMatrix()


def draw_floor(game_map):
    glColor3f(0.25, 0.25, 0.25)
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(game_map.width, 0, 0)
    glVertex3f(game_map.width, 0, game_map.height)
    glVertex3f(0, 0, game_map.height)
    glEnd()


def render(game_map, player):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glRotatef(player.pitch, 1, 0, 0)
    glRotatef(-player.yaw, 0, 1, 0)
    glTranslatef(
        -player.x,
        -player.h,
        -player.y
    )
    draw_floor(game_map)
    for y, row in enumerate(game_map.grid):
        for x, cell in enumerate(row):
            if cell == 1:
                draw_cube(x, y)

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
    game_map = MapData()
    game_map.load(MAP_FILE)

    player = Player(
        game_map.player_spawn[0],
        game_map.player_spawn[1]
    )

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
                    -120,
                    min(120, player.pitch)
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
        render(
            game_map,
            player
        )
        pygame.display.flip()

if __name__ == "__main__":
    main()