import re

data = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def main(data):
    lines = data.strip().split("\n")
 
    # find all individual symbol coordinates
    symbols = []
    for i, line in enumerate(lines):
        for match in re.finditer("[^\d\.]", line):
            symbols.append((i, match.start()))
 
    # find all numbers (groups)
    numbers = []
    for i, line in enumerate(lines):
        for match in re.finditer("\d+", line):
            numbers.append((match.group(), i, match.start(), match.end()))

    res = 0

    for number in numbers:
        connected = False
        for y in [number[1]-1, number[1], number[1]+1]:
            for x in range(number[2]-1, number[3]+1):
                for symbol in symbols:
                    if symbol[0] == y and symbol[1] == x:
                        connected = True
                        break
        if connected:
            res += int(number[0])

    print(res)


if __name__ == "__main__":
    data = open("./input.txt", "r").read()
    main(data)

