data = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""


SLOPES = "^v<>"
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]


RES = []


def show(matrix, path=None):
    bg = "\033[90m"
    fg = "\033[1m"
    clr = "\033[0;0m"
    print()
    space = " " if len(matrix) < 100 else ""
    for i, row in enumerate(matrix):
        if i == 0:
            print("  ", end="")
            for n, _ in enumerate(row):
                print(f"{(n % 10)}", end=space)
            print()
        print(f"{(i % 10)}", end=" ")
        for j, cell in enumerate(row):
            if path and (i, j) in path:
                print(f"{fg}◼{clr}", end=space)
            else:
                print(f"{bg}{cell}{clr}", end=space)
        print()


def get_possible_moves(map: list[list[str]], pos: tuple, visited: list) -> list[tuple]:
    """
    Check the map around the "pos" position.
    Try to move U, D, R, L. The move is possible if:
    - the next point is on the map
    - it is not a tree ("#")
    - it was not visited
    - if the current pos is an arrow, move only in this direction
    """
    size = len(map)
    pos_options = []

    try:
        move = MOVES[SLOPES.index(map[pos[0]][pos[1]])]
        i, j = pos[0] + move[0], pos[1] + move[1]
        if (i, j) not in visited and map[i][j] != "#":
            pos_options.append((i, j))
        return pos_options
    except ValueError:
        pass

    for move in MOVES:
        i, j = pos[0] + move[0], pos[1] + move[1]
        if i < 0 or i >= size or j < 0 or j >= size:
            continue
        if map[i][j] == "#":
            continue
        if (i, j) not in visited:
            pos_options.append((i, j))

    return pos_options


def walker(field, pos, end, visited) -> list[tuple]:
    global RES

    visited.append(pos)

    while pos != end:
        moves = get_possible_moves(field, pos, visited)
        # sleep(0.1)

        if not moves:
            return []

        elif len(moves) == 1:
            pos = moves[0]
            visited.append(pos)

        else:
            # check all paths from the junction, use the longest path
            paths = [walker(field, s, end, visited.copy()) for s in moves]
            # print("paths:", tuple(map(len, paths)))
            return []  # sorted(paths, key=lambda el: len(el))[-1]

    if pos == end:
        RES.append(visited)
        print(f"END {len(visited)}")
        return visited
    else:
        return []


def main(data):
    matrix = tuple(tuple(row) for row in data.splitlines())

    size = len(matrix)
    start = (0, 1)
    end = (size - 1, size - 2)

    path = walker(matrix, start, end, [])

    paths = sorted(RES, key=lambda el: len(el), reverse=True)

    for path in paths[:1]:
        print()
        print()
        print(len(path))
        show(matrix, path)


if __name__ == "__main__":
    # data = open("day_23/input").read()
    main(data.strip())
#
