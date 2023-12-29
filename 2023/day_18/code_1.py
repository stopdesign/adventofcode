data = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


class Field:
    moves = {
        "U": (-1, 0),
        "R": (0, +1),
        "D": (+1, 0),
        "L": (0, -1),
    }

    def __init__(self):
        self.holes = []
        self.pos = [0, 0]
        self.path = [(0, 0)]

    def __str__(self):
        lines = ["".join(r) for r in self.m]
        return "\n".join(lines)

    def render_map(self):
        coords = zip(*self.path)
        ii = next(coords)
        jj = next(coords)

        min_i = min(ii)
        min_j = min(jj)

        m = []
        for i in range(min(ii), max(ii) + 1):
            row = ["."] * (max(jj) - min(jj) + 1)
            m.append(row)

        for pos in self.path:
            m[pos[0] - min_i][pos[1] - min_j] = "#"

        self.m = m

    def digg(self, direction, steps, color):
        move = self.moves[direction]
        for n in range(steps):
            self.pos[0] += move[0]
            self.pos[1] += move[1]
            self.path.append(list(self.pos))
            # print(self.pos)

    def digg_all(self, steps):
        for step in steps:
            direction, steps, color = step.split()
            color = color.strip("(").strip(")")
            self.digg(direction, int(steps), color)

    def fill_connected(self, start_i, start_j):
        stack = [(start_i, start_j)]
        grid = range(len(self.m))

        while stack:
            i, j = stack.pop()

            if self.m[i][j] != ".":
                continue

            self.m[i][j] = "#"

            for dr, dc in self.moves.values():
                new_i, new_j = i + dr, j + dc
                if new_i in grid and new_j in grid:
                    stack.append((new_i, new_j))

    def fill_inside(self):
        for i, row in enumerate(self.m):
            if row[0] == "#" and row[1] == ".":
                break
        # found enclosed cell
        return self.fill_connected(i, 1)


def main(data):
    field = Field()
    field.digg_all(data.splitlines())
    field.render_map()
    field.fill_inside()
    print(field)
    print(str(field).count("#"))


# data = open("day_18/input").read()
main(data.strip())
#
