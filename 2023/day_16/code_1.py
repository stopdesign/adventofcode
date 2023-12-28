from dataclasses import dataclass

data = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


@dataclass
class Beam:
    i: int = 0
    j: int = 0
    dir: str = ">"


class Field:
    def __init__(self, data, start_pos, start_dir):
        self.m_base = [list(row) for row in data.splitlines()]
        self.m_beam = [["."] * len(row) for row in data.splitlines()]

        # start
        self.beams = [Beam(start_pos[0], start_pos[1], start_dir)]
        self.m_beam[start_pos[0]][start_pos[1]] = start_dir

    def __str__(self):
        res = "\n"
        base_lines = [" ".join(r) for r in self.m_base]
        beam_lines = [" ".join(r) for r in self.m_beam]
        for r1, r2 in zip(base_lines, beam_lines):
            res += f"{r1}      {r2}\n"
        return res

    def move_straight(self, beam):
        if beam.dir == ">":
            beam.j += 1

        if beam.dir == "<":
            beam.j -= 1

        if beam.dir == "v":
            beam.i += 1

        if beam.dir == "^":
            beam.i -= 1

    def update_beam(self, beam):
        cell = self.m_base[beam.i][beam.j]

        # splitter
        if cell == "|":
            if beam.dir in "<>":
                self.beams.append(Beam(beam.i + 1, beam.j, "v"))
                beam.dir = "^"
                self.move_straight(beam)
            else:
                self.move_straight(beam)

        # splitter
        elif cell == "-":
            if beam.dir in "^v":
                self.beams.append(Beam(beam.i, beam.j + 1, ">"))
                beam.dir = "<"
                self.move_straight(beam)
            else:
                self.move_straight(beam)

        # mirror
        elif cell == "/":
            # rotate the beam
            if beam.dir == ">":
                beam.dir = "^"
            elif beam.dir == "<":
                beam.dir = "v"
            elif beam.dir == "v":
                beam.dir = "<"
            elif beam.dir == "^":
                beam.dir = ">"
            self.move_straight(beam)

        # mirror
        elif cell == "\\":
            # rotate the beam
            if beam.dir == ">":
                beam.dir = "v"
            elif beam.dir == "<":
                beam.dir = "^"
            elif beam.dir == "v":
                beam.dir = ">"
            elif beam.dir == "^":
                beam.dir = "<"
            self.move_straight(beam)

        # empty cell
        elif cell == ".":
            self.move_straight(beam)

    def step(self):
        # atomic beam moves (process splitted beam in one step)
        for beam in list(self.beams):
            self.update_beam(beam)

        # filter out beams from outside of the grid
        grid = range(len(self.m_beam))
        self.beams = list(filter(lambda b: b.i in grid and b.j in grid, self.beams))

        # filter out beams on known paths
        # FIX: now m_beam stores only the last direction
        self.beams = list(filter(lambda b: self.m_beam[b.i][b.j] != b.dir, self.beams))

        # Show new beam(s) on the map
        for b in self.beams:
            self.m_beam[b.i][b.j] = b.dir

        return bool(self.beams)

    def get_max_cnt(self):
        while self.step():
            pass
        dots_cnt = str(self.m_beam).count(".")
        return len(self.m_beam) * len(self.m_beam[0]) - dots_cnt


def main(data):
    max_cnt = 0
    grid_size = data.count("\n") + 1

    for i in range(grid_size):
        field = Field(data, (i, 0), ">")
        max_cnt = max(max_cnt, field.get_max_cnt())

        field = Field(data, (i, grid_size - 1), "<")
        max_cnt = max(max_cnt, field.get_max_cnt())

        field = Field(data, (0, i), "v")
        max_cnt = max(max_cnt, field.get_max_cnt())

        field = Field(data, (grid_size - 1, i), "^")
        max_cnt = max(max_cnt, field.get_max_cnt())

    print(max_cnt)


if __name__ == "__main__":
    # data = open("day_16/input").read()
    main(data.strip())
#
