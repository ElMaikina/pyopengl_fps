import csv


class Level:
    def __init__(self):
        self.grid = []
        self.width = 0
        self.height = 0
        self.player_spawn = (1.5, 1.5)

    def load(self, filename):
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            self.grid = []
            last_player = None

            for y, row in enumerate(reader):
                parsed_row = []

                for x, value in enumerate(row):
                    try:
                        v = int(value)
                    except:
                        v = 0

                    if v == 2:
                        last_player = (x + 0.5, y + 0.5)
                        parsed_row.append(0)
                    elif v == 1:
                        parsed_row.append(1)
                    else:
                        parsed_row.append(0)

                self.grid.append(parsed_row)

        self.height = len(self.grid)
        self.width = max(len(r) for r in self.grid)

        if last_player is not None:
            self.player_spawn = last_player

    def is_wall(self, x, y):
        gx = int(x)
        gy = int(y)

        if gx < 0 or gy < 0:
            return True
        if gy >= self.height:
            return True
        if gx >= len(self.grid[gy]):
            return True

        return self.grid[gy][gx] == 1