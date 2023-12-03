import re

data = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""


def check_line(line):
    if line := re.sub(r"[^\d]+", "", line):
        return int(line[0] + line[-1])
    return 0


def main(data):

    res = 0

    for line in data.strip().split("\n"):
        res += check_line(line)

    print(res)


if __name__ == "__main__":
    data = open("./input.txt", "r").read()
    main(data)

