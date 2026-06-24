import math

from colision import collide_circle


PARTICLE_RADIUS = 0.05


class Particle:
    def __init__(self, x, y, vx, vy, life=1.0):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.life = life
        self.active = True

    def update(self, game_map, dt):
        if not self.active:
            return

        self.life -= dt

        if self.life <= 0:
            self.active = False
            return

        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt

        if collide_circle(new_x, new_y, PARTICLE_RADIUS, game_map):
            self.active = False
            return

        self.x = new_x
        self.y = new_y