data = """ 
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def symmetry_line_index(pattern: list[str]) -> int:
    """
    Returns the index of the row that is the horizontal symmetry line.
    """
    for i in range(1, len(pattern)):
        before = pattern[:i]
        after = pattern[i:]

        min_len = min(len(before), len(after))
        if after[:min_len] == before[::-1][:min_len]:
            return i
            
    return 0


def transpose(pattern: list[str]) -> list[str]:
    return ["".join(x) for x in zip(*pattern)]


def main(data):
    patterns = data.split("\n\n")
    res = 0
    for pattern in patterns:
        pattern = pattern.strip().split("\n")
        sym_h = symmetry_line_index(pattern)
        sym_v = symmetry_line_index(transpose(pattern))
        # print(sym_v, sym_h)
        res += sym_v + sym_h * 100
    print(res)


if __name__ == "__main__":
    data = open("day_13/input").read()
    main(data)
