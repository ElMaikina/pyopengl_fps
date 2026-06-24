from fisicas_cpu import update_entities_cpu


def update_entities_gpu(enemies, items, particles, player, game_map, dt):
    """
    Versión GPU.

    Aquí más adelante se enviarán los datos de enemigos, items
    o partículas a OpenCL/CUDA.

    Por ahora usa la versión CPU como respaldo para que el juego
    siga funcionando.
    """

    update_entities_cpu(
        enemies,
        items,
        particles,
        player,
        game_map,
        dt
    )