"""
The key point is to find the periodicity of the matrix rotation results.
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


def sort_row(row):
    pos = 0
    for j in range(len(row)):
        if row[j] == "O":
            if j != pos:
                row[j] = "."
                row[pos] = "O"
            pos += 1
        elif row[j] == "#":
            pos = j + 1
    return row


def sort_w(matrix):
    return [sort_row(r) for r in matrix]


def calc_load(matrix):
    load = 0
    size = len(matrix)
    for i, ln in enumerate(matrix):
        load += ln.count("O") * (size - i)
    return load


def rotate_r(matrix):
    list_of_tuples = zip(*matrix[::-1])
    return [list(t) for t in list_of_tuples]


def rotate_l(m):
    for i in range(3):
        m = rotate_r(m)
    return m


def main(lines):
    # I assume the matrix is square
    assert len(lines) == len(lines[0])

    ll = list(map(list, lines))

    # Part 1 solution
    # ll = rotate_l(ll)
    # sort_w(ll)
    # ll = rotate_r(ll)

    # Change the initial orientation,
    # as it is convinient to sort matrix to the left (west)
    ll = rotate_l(ll)

    cnt = 0  # rotations_counter
    target_cnt = 1_000_000_000
    matrix_states = []

    while cnt <= target_cnt:
        state_hash = str(ll)  # the actual hash would do the same

        # detect period in states
        # break if current state is the same as the one we need
        if state_hash in matrix_states:
            period = cnt - matrix_states.index(state_hash)
            if (target_cnt - cnt) % period == 0:
                break

        matrix_states.append(state_hash)
        cnt += 1

        # one round of N-W-S-E transformations
        for i in range(4):
            ll = rotate_r(sort_w(ll))

    # change the rotation back
    ll = rotate_r(ll)

    print("Load:", calc_load(ll))


if __name__ == "__main__":
    # data = open("day_14/input").read()
    main(data.strip().split())
#
