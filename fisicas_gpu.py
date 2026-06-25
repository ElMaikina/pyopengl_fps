import numpy as np
import pyopencl as cl


ENEMY_SPEED = 1.2


class GPUPhysics:
    def __init__(self):
        platforms = cl.get_platforms()

        platform = None
        for p in platforms:
            if "NVIDIA" in p.name.upper():
                platform = p
                break

        if platform is None:
            platform = platforms[0]

        device = platform.get_devices()[0]

        print(f"Usando plataforma OpenCL: {platform.name}")
        print(f"Usando dispositivo OpenCL: {device.name}")

        self.context = cl.Context([device])
        self.queue = cl.CommandQueue(self.context)

        with open("kernels.cl", "r", encoding="utf-8") as f:
            kernel_code = f.read()

        self.program = cl.Program(
            self.context,
            kernel_code
        ).build()

    def update_enemies_gpu(self, enemies, player, dt):
        n = len(enemies)

        if n == 0:
            return

        enemy_x = np.array(
            [enemy.x for enemy in enemies],
            dtype=np.float32
        )

        enemy_y = np.array(
            [enemy.y for enemy in enemies],
            dtype=np.float32
        )

        mf = cl.mem_flags

        enemy_x_buffer = cl.Buffer(
            self.context,
            mf.READ_WRITE | mf.COPY_HOST_PTR,
            hostbuf=enemy_x
        )

        enemy_y_buffer = cl.Buffer(
            self.context,
            mf.READ_WRITE | mf.COPY_HOST_PTR,
            hostbuf=enemy_y
        )

        self.program.update_enemies_gpu(
            self.queue,
            (n,),
            None,
            enemy_x_buffer,
            enemy_y_buffer,
            np.float32(player.x),
            np.float32(player.y),
            np.float32(dt),
            np.float32(ENEMY_SPEED),
            np.int32(n)
        )

        cl.enqueue_copy(
            self.queue,
            enemy_x,
            enemy_x_buffer
        )

        cl.enqueue_copy(
            self.queue,
            enemy_y,
            enemy_y_buffer
        )

        self.queue.finish()

        for i, enemy in enumerate(enemies):
            enemy.x = float(enemy_x[i])
            enemy.y = float(enemy_y[i])

    def update_entities_gpu(
        self,
        enemies,
        items,
        particles,
        player,
        game_map,
        dt
    ):
        self.update_enemies_gpu(
            enemies,
            player,
            dt
        )

        for item in items:
            item.update(player)

        for particle in particles:
            particle.update(game_map, dt)

        particles[:] = [
            particle for particle in particles
            if particle.active
        ]