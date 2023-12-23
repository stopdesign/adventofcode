import json
import math
from time import monotonic, sleep

data = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##...####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

data = """
.............
..#......###.
.##.......##.
.......#...#.
....#........
....#...##...
......S......
........#....
....##.##....
.#...#.....#.
.##..........
.#.......#...
.............
"""

# data = data.replace("#", ".")


class Matrix:
    def __init__(self, data, n=1, s=None):
        self.size = len(data)
        self.m = data
        self.moves = (
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        )
        self.m = self._repeat(n)
        self.m = json.loads(json.dumps(self.m))

        h = len(self.m) // 2
        if s:
            self.m[s[0]][s[1]] = "O"  # set start
        else:
            self.m[h][h] = "O"

        self.edge = [self.find_start()]

    def __str__(self):
        res = ""
        h = len(self.m) // 2
        for i, row in enumerate(self.m, 1):
            row_str = ""
            for j, ch in enumerate(row, 1):
                row_str += ch
                if j % self.size == 0:
                    row_str += " "
            res += f"{row_str}\n"
            if i % self.size == 0:
                res += "\n"

        res = res.replace(".", "∙")
        res = res.replace("#", "⊡")
        res = res.replace("O", "▪")
        return res

    def find_start(self):
        for i, row in enumerate(self.m):
            if "O" in row:
                return (i, row.index("O"))

    def _repeat(self, times):
        for i in range(len(self.m)):
            self.m[i] = self.m[i] * times
        return self.m * times

    @property
    def cnt(self):
        return repr(self.m).count("O")

    def step(self):
        new_edge = []

        # enter new cells
        for cell in self.edge:
            for move in self.moves:
                i = cell[0] + move[0]
                j = cell[1] + move[1]
                if i < 0 or j < 0:
                    continue
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
    target = 600
    w = len(data)
    g = (target - w // 2) / w
    s = 2 * int(math.ceil(g)) + 1

    # s = 1

    m = Matrix(data, s)
    # print(m)
    prev = 0
    for i in range(target):
        m.step()
        # print("\n" * 10)
        cnt = m.cnt
        # diff = cnt - prev
        opt = ""
        if (i + 1 + w // 2) % w == 0:
            opt = "--------"
        if (i + 0) % w == 0:
            opt = "========"
        prev = cnt
        cnt_no_bars = (i + 2) ** 2
        diff = cnt_no_bars - cnt
        print(f"step:{(i+1):>5}   cnt:{cnt:>6}   max:{cnt_no_bars:>6}  {opt}")

    print()
    # print(m)
    print(m.cnt)


def get_load(data, combo, steps=0):
    h = len(data) // 2

    print(combo, h, steps)

    # full center
    if combo == "c":
        m = Matrix(data)
        for n in range(h * 2 + 1):
            # print("c", n)
            m.step()
        return m.cnt

    # full nun-center
    if combo == "n":
        m = Matrix(data)
        for n in range(h * 2):
            # print("n", n)
            m.step()
        return m.cnt

    if combo == "4d" and steps:
        cnt = 0
        for s in [(0, 0), (0, -1), (-1, 0), (-1, -1)]:
            m = Matrix(data, s=s)
            for n in range(steps):
                # print("d", s, n)
                m.step()
            cnt += m.cnt
        return cnt

    if combo == "4s" and steps:
        cnt = 0
        for s in [(0, h), (-1, h), (h, 0), (h, -1)]:
            m = Matrix(data, s=s)
            for n in range(steps):
                # print("s", s, n)
                m.step()
            cnt += m.cnt
        return cnt

    raise ValueError("bad get_load params")


def calc(data):
    w = len(data)
    h = (w - 1) // 2

    mult = 6
    add = 0
    target = h + w * mult + add
    # target = 65 + 131 * 202300
    target = 26501365
    # target = 197 + 65

    n = target
    n2 = n - h
    n1 = n - w
    n0 = n - w - h

    g = (n0 - h) / w
    gc = int(math.ceil(g))
    s = 2 * gc + 1

    f_n = gc**2
    f_c = (gc + 1) ** 2

    if n % 2:
        f_c, f_n = f_n, f_c

    c3_cnt = math.ceil((n0 + 0) / w)
    c5_cnt = math.ceil((n2 + 0) / w)

    print(f"\nn: {n}, n2: {n2}, n1: {n1}, n0: {n0}\n")
    print("cnts:", c3_cnt, c3_cnt, "\n")

    c1, c2, c3, c4, c5 = 0, 0, 0, 0, 0

    # количество элементов в стабильных конфигурациях
    c1 = get_load(data, "c")
    c2 = get_load(data, "n")

    c3 = get_load(data, "4d", steps=n - n0 - 1)
    c4 = get_load(data, "4s", steps=n - n1 - 1)
    c5 = get_load(data, "4d", steps=n - n2 - 1)

    print()
    print(f"points: {c1:>8} {c2:>8} {c3:>8} {c4:>8} {c5:>8}")
    print(f"counts: {f_c:>8} {f_n:>8} {c3_cnt:>8f} {1:>8} {c5_cnt:>8f}")
    print()

    count_n = c1 * f_c + c2 * f_n + c3 * c3_cnt + c4 + c5 * c5_cnt

    print(f"n: {n}  n0: {n0}  g: {g:.03f}  s: {s}  gc: {gc}   f: {f_c} + {f_n}")

    print(f"count_n {count_n}")


if __name__ == "__main__":
    t1 = monotonic()
    data = open("day_21/input").read()
    # data = data.replace("#", ".")
    data = data.replace("S", ".")
    data = [list(row) for row in data.strip().splitlines()]
    # main(data)
    calc(data)

    print(f"\ntime: {(monotonic() - t1):.02f} s")

#
