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


def symmetry_line_index(pattern: list[str], smudge_cnt=0) -> int:
    """
    Returns the index of the row that is the horizontal symmetry line.
    """
    for i in range(1, len(pattern)):
        before = pattern[:i]
        after = pattern[i:]

        min_common_size = min(len(before), len(after))

        a_lines = after
        b_lines = before[::-1]

        # Count difference between A and B patterns
        diff = 0
        for j in range(min_common_size):
            diff += sum(1 for a, b in zip(a_lines[j], b_lines[j]) if a != b)

        if diff == smudge_cnt:
            return i

    return 0


def transpose(pattern: list[str]) -> list[str]:
    return ["".join(x) for x in zip(*pattern)]


def main(data):
    patterns = data.split("\n\n")
    res = 0
    smudge_cnt = 1
    for pattern in patterns:
        pattern = pattern.strip().split("\n")
        transposed_pattern = transpose(pattern)
        sym_h = symmetry_line_index(pattern, smudge_cnt)
        sym_v = symmetry_line_index(transposed_pattern, smudge_cnt)
        # print(sym_v, sym_h)
        res += sym_v + sym_h * 100
    print(res)


if __name__ == "__main__":
    data = open("day_13/input").read()
    main(data)
