import math
import numpy as np
from pygame.locals import *

from colision import collide_circle


PLAYER_RADIUS = 0.25
PLAYER_HEIGHT = 0.4

ACCELERATION = 15.0
DECELERATION = 15.0
MAX_SPEED = 4.0


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vx = 0.0
        self.vy = 0.0

        self.yaw = 0.0
        self.pitch = 0.0

        self.h = PLAYER_HEIGHT

        self.forward_speed = 0.0
        self.strafe_speed = 0.0

        self.score = 0
        self.health = 100

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
        if keys[K_w]:
            self.forward_speed -= ACCELERATION * dt
        elif keys[K_s]:
            self.forward_speed += ACCELERATION * dt
        else:
            self.forward_speed = self.apply_deceleration(
                self.forward_speed,
                dt
            )

        if keys[K_d]:
            self.strafe_speed += ACCELERATION * dt
        elif keys[K_a]:
            self.strafe_speed -= ACCELERATION * dt
        else:
            self.strafe_speed = self.apply_deceleration(
                self.strafe_speed,
                dt
            )

        speed = math.hypot(
            self.forward_speed,
            self.strafe_speed
        )

        if speed > MAX_SPEED:
            factor = MAX_SPEED / speed
            self.forward_speed *= factor
            self.strafe_speed *= factor

        forward = self.forward_vector()
        right = self.right_vector()

        velocity = forward * self.forward_speed + right * self.strafe_speed

        self.vx = velocity[0]
        self.vy = velocity[1]

        self.move_with_collision(dt, game_map)

    def apply_deceleration(self, speed, dt):
        if speed > 0:
            return max(0, speed - DECELERATION * dt)

        if speed < 0:
            return min(0, speed + DECELERATION * dt)

        return 0

    def move_with_collision(self, dt, game_map):
        new_x = self.x + self.vx * dt

        if not collide_circle(new_x, self.y, PLAYER_RADIUS, game_map):
            self.x = new_x

        new_y = self.y + self.vy * dt

        if not collide_circle(self.x, new_y, PLAYER_RADIUS, game_map):
            self.y = new_y