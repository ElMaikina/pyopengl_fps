from OpenGL.GL import *


def draw_cube(x, y):
    glPushMatrix()
    glTranslatef(x + 0.5, 0.5, y + 0.5)

    glBegin(GL_QUADS)

    glColor3f(0.7, 0.7, 0.7)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)

    glColor3f(0.8, 0.2, 0.2)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glColor3f(0.2, 0.8, 0.2)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    glColor3f(0.2, 0.2, 0.8)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

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


def draw_enemy(enemy):
    if not enemy.alive:
        return

    glPushMatrix()
    glTranslatef(enemy.x, 0.35, enemy.y)
    glScalef(0.5, 0.7, 0.5)

    glBegin(GL_QUADS)

    glColor3f(1.0, 0.0, 0.0)

    # FRONT
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # BACK
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)

    # LEFT
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    # RIGHT
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    # TOP
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)

    # BOTTOM
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glEnd()

    glPopMatrix()


def draw_item(item):
    if not item.active:
        return

    glColor3f(0.0, 1.0, 1.0)

    glPushMatrix()
    glTranslatef(item.x, 0.2, item.y)

    glBegin(GL_QUADS)

    glVertex3f(-0.15, -0.15, 0.0)
    glVertex3f(0.15, -0.15, 0.0)
    glVertex3f(0.15, 0.15, 0.0)
    glVertex3f(-0.15, 0.15, 0.0)

    glEnd()

    glPopMatrix()


def draw_particle(particle):
    if not particle.active:
        return

    glColor3f(1.0, 1.0, 0.0)

    glPushMatrix()
    glTranslatef(particle.x, 0.2, particle.y)

    glBegin(GL_QUADS)

    glVertex3f(-0.05, -0.05, 0.0)
    glVertex3f(0.05, -0.05, 0.0)
    glVertex3f(0.05, 0.05, 0.0)
    glVertex3f(-0.05, 0.05, 0.0)

    glEnd()

    glPopMatrix()


def render(game_map, player, enemies, items, particles):
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

    for item in items:
        draw_item(item)

    for enemy in enemies:
        draw_enemy(enemy)

    for particle in particles:
        draw_particle(particle)