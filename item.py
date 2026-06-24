import math


ITEM_RADIUS = 0.3


class Item:
    def __init__(self, x, y, item_type="score"):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.active = True

    def update(self, player):
        if not self.active:
            return

        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance < ITEM_RADIUS:
            self.apply_effect(player)
            self.active = False

    def apply_effect(self, player):
        if self.item_type == "score":
            player.score += 10

        elif self.item_type == "health":
            player.health = min(100, player.health + 20)