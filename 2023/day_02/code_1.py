import re

data = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

CUBES = {"red": 12, "green": 13, "blue": 14}


def is_valid_round(round_data):
    for color_data in round_data.split(","):
        cnt, color = color_data.strip().split(" ")
        if int(cnt) > CUBES.get(color, 0):
            return False
    return True


def check_line(line):
    if mtc := re.match(r"Game (\d+): (.*)", line):
        game_id = int(mtc.group(1))
        game_data = mtc.group(2)
        rounds_data = game_data.split(";")
        rounds_validity = map(is_valid_round, rounds_data)
        if all(rounds_validity):
            return game_id
    return 0


def main(data):
    res = 0

    for line in data.strip().split("\n"):
        res += check_line(line)

    print(res)


if __name__ == "__main__":
    data = open("./input.txt", "r").read()
    main(data)
