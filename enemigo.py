import math

from colision import collide_circle


ENEMY_RADIUS = 0.25
ENEMY_SPEED = 1.2
ENEMY_DAMAGE_DISTANCE = 0.45


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vx = 0.0
        self.vy = 0.0

        self.alive = True

    def update(self, player, game_map, dt):
        if not self.alive:
            return

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0.001:
            self.vx = (dx / distance) * ENEMY_SPEED
            self.vy = (dy / distance) * ENEMY_SPEED
        else:
            self.vx = 0.0
            self.vy = 0.0

        new_x = self.x + self.vx * dt

        if not collide_circle(new_x, self.y, ENEMY_RADIUS, game_map):
            self.x = new_x

        new_y = self.y + self.vy * dt

        if not collide_circle(self.x, new_y, ENEMY_RADIUS, game_map):
            self.y = new_y

        if distance < ENEMY_DAMAGE_DISTANCE:
            player.health -= 1