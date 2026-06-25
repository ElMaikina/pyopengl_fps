__kernel void update_enemies_gpu(
    __global float* enemy_x,
    __global float* enemy_y,
    float player_x,
    float player_y,
    float dt,
    float speed,
    int n
)
{
    int id = get_global_id(0);

    if (id >= n) {
        return;
    }

    float dx = player_x - enemy_x[id];
    float dy = player_y - enemy_y[id];

    float distance = sqrt(dx * dx + dy * dy);

    if (distance > 0.001f) {
        enemy_x[id] += (dx / distance) * speed * dt;
        enemy_y[id] += (dy / distance) * speed * dt;
    }
}