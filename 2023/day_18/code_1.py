import re

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

MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]

RX = re.compile("#(\w+)(\d)")


def polygon_area(path):
    """
    Shoelace formula modified for a polygon with borders.
    """
    area = 0
    perimeter = 0
    for n in range(len(path)):
        i, j = path[n], path[n - 1]
        area += i[0] * j[1] - j[0] * i[1]
        perimeter += abs(i[0] - j[0]) + abs(i[1] - j[1])
    area = (abs(area) + perimeter) // 2 + 1
    return area


def follow_the_plan(dig_plan):
    i, j = 0, 0
    path = []
    for step in RX.findall(dig_plan):
        length = int(step[0], 16)  # hex to int
        direction = int(step[1])
        d_i, d_j = MOVES[direction]
        i += d_i * length
        j += d_j * length
        path.append((i, j))
    return path


def main(dig_plan):
    path = follow_the_plan(dig_plan)
    area = polygon_area(path)
    print(area)


# data = open("day_18/input").read()
main(data.strip())
#
