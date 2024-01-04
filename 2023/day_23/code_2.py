from time import monotonic

import networkx as nx

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


def show(matrix, path=None):
    bg = "\033[90m"
    fg = "\033[1m"
    clr = "\033[0;0m"
    print()
    path = path or {}
    space = " " if len(matrix) < 100 else ""
    path = set(path)
    for i, row in enumerate(matrix):
        if i == 0:
            print("  ", end="")
            for n, _ in enumerate(row):
                print(f"{(n % 10)}", end=space)
            print()
        print(f"{(i % 10)}", end=" ")
        for j, cell in enumerate(row):
            if (i, j) in path:
                print(f"{fg}∎{clr}", end=space)
            else:
                print(f"{bg}{cell}{clr}", end=space)
        print()
    print("path len", len(path), "\n")


def get_connected(map: list[list[str]], pos: tuple) -> list[tuple]:
    size = len(map)
    for move in (-1, 0), (1, 0), (0, -1), (0, 1):
        i, j = pos[0] + move[0], pos[1] + move[1]
        if i < 0 or i >= size or j < 0 or j >= size:
            continue
        if map[i][j] == "#":
            continue
        yield (i, j)


def main(data):
    matrix = tuple(tuple(row) for row in data.splitlines())

    size = len(matrix)
    grid = range(size)
    start = (0, 1)
    end = (size - 1, size - 2)

    # get all valid cells (nodes)
    good_cells = iter((i, j) for i in grid for j in grid if matrix[i][j] != "#")

    # convert matrix into graph
    graph = {node: get_connected(matrix, node) for node in good_cells}

    gnx = nx.Graph(graph)

    # all edges are 1
    for a, b in gnx.edges():
        gnx[a][b]["w"] = 1

    # nodes with exactly two neighbors
    nodes_to_remove = [node for node, d in dict(gnx.degree()).items() if d == 2]

    # connect siblings of each removed node directly
    for node in nodes_to_remove:
        if gnx.degree(node) == 2:
            n1, n2 = gnx.neighbors(node)
            w = gnx[node][n1]["w"] + gnx[node][n2]["w"]
            gnx.add_edge(n1, n2, w=w)
            gnx.remove_node(node)

    # show(matrix, list(gnx))

    max_w = 0
    for path in nx.all_simple_paths(gnx, start, end):
        total_w = 0
        for i, node in enumerate(path):
            if i > 0:
                prev = path[i - 1]
                w = gnx[prev][node].get("w", 0)
                total_w += w
        # print(path, total_w)
        max_w = max(max_w, total_w)
        # show(matrix, p)

    print("res:", max_w)


if __name__ == "__main__":
    t1 = monotonic()
    # data = open("day_23/input").read()
    main(data.strip())
    print(f"\ntime: {(monotonic() - t1):.03f} s")
#
