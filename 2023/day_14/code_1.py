"""
The idea is to split each string by #,
sort each part, than reassemble the string with #.
"""

data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def transpose(matrix: list[str]) -> list[str]:
    return ["".join(x) for x in zip(*matrix)]


def sort_part(line):
    return "".join(sorted(list(line), reverse=True))


def process_line(line):
    return "#".join(map(sort_part, line.split("#")))


def main(lines):
    new_lines = map(process_line, transpose(lines))

    load = 0
    for i, ln in enumerate(transpose(new_lines)):
        n = len(lines[0]) - i
        load += ln.count("O") * n

    print(load)


if __name__ == "__main__":
    data = open("day_14/input").read()
    main(data.strip().split())
