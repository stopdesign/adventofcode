data = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


class Matrix:

    def __init__(self, data):
        self.m = data
        self.edge = [self.find_start()]
        self.moves = (
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        )

    def __str__(self):
        res = ""
        for row in self.m:
            res += "".join(row) + "\n"
        return res

    def find_start(self):
        for i, row in enumerate(self.m):
            if "O" in row:
                return (i, row.index("O"))

    def step(self):
        new_edge = []

        # enter new cells
        for cell in self.edge:
            for move in self.moves:
                i = cell[0] + move[0]
                j = cell[1] + move[1]
                try:
                    if self.m[i][j] == ".":
                        new_edge.append((i, j))
                        self.m[i][j] = "O"
                except IndexError:
                    pass

        # exit visited cells
        for cell in self.edge:
            if cell not in new_edge:
                self.m[cell[0]][cell[1]] = "."

        # print(len(new_edge))

        self.edge = new_edge


def main(data):
    m = Matrix(data)
    # print(m)
    for i in range(64):
        m.step()
    # print(m)
    print(str(m).count("O"))


if __name__ == "__main__":
    # data = open("day_21/input").read()
    data = data.replace("S", "O")
    data = [list(row) for row in data.strip().splitlines()] 
    main(data)

#
