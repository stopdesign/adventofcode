import re

data = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

CUBES = {"red": 0, "green": 0, "blue": 0}


def get_min_set_power(rounds_data):
    mins = dict(CUBES)

    for round_data in rounds_data:
        for color_data in round_data.split(","):
            cnt, color = color_data.strip().split(" ")
            mins[color] = max(mins[color], int(cnt))

    res = 1
    for min_val in mins.values():
        res *= min_val
    
    return res


def check_line(line):
    res = 0
    if mtc := re.match(r"Game (\d+): (.*)", line):
        game_data = mtc.group(2)
        rounds_data = game_data.split(";")
        res += get_min_set_power(rounds_data)
    return res


def main(data):
    res = 0

    for line in data.strip().split("\n"):
        res += check_line(line)

    print(res)


if __name__ == "__main__":
    data = open("./input.txt", "r").read()
    main(data)
