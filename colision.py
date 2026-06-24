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