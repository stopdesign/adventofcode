from itertools import combinations

data = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

# GAP_MULTIPLIER = 2  # part 1, double the gap size
GAP_MULTIPLIER = 1000000  # part 2


def find_gaps(grid, star="#") -> tuple:
    """
    Gap is a row or column without a "star".
    """
    cols = len(grid[0])
    gaps_i = [i for i in range(cols) if star not in grid[i]]
    gaps_j = [j for j in range(cols) if star not in [row[j] for row in grid]]
    return gaps_i, gaps_j


def has_gap(a: int, b: int, gap: int) -> bool:
    """
    Checks if the gap is between these points.
    """
    return a < gap < b or b < gap < a


def distance(a: tuple, b: tuple, gaps: tuple) -> int:
    """
    Calculates the Manhattan distance between two points A and B.
    Add extra rows/cols if there are gaps between the two points.
    """
    m = GAP_MULTIPLIER - 1

    gaps_i = sum(has_gap(a[0], b[0], gap) for gap in gaps[0])
    gaps_j = sum(has_gap(a[1], b[1], gap) for gap in gaps[1])

    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + (gaps_i + gaps_j) * m


def star_coords(grid, star="#"):
    """
    Returns a list of coordinates of the stars.
    """
    coords = []
    for i, line in enumerate(grid):
        for j, tile in enumerate(line):
            if tile == star:
                coords.append((i, j))
    return coords


def main(grid):
    gaps = find_gaps(grid)
    coords = star_coords(grid)
    pairs = combinations(coords, 2)
    res = sum(distance(*pair, gaps) for pair in pairs)
    print("res", res)


if __name__ == "__main__":
    # data = open("input.txt").read()
    grid = data.strip().splitlines()
    main(grid)
