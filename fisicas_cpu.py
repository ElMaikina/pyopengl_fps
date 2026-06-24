def update_entities_cpu(enemies, items, particles, player, game_map, dt):
    for enemy in enemies:
        enemy.update(player, game_map, dt)

    for item in items:
        item.update(player)

    for particle in particles:
        particle.update(game_map, dt)

    particles[:] = [p for p in particles if p.active]