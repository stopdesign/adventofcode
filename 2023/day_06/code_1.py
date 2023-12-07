import re

data = """ 
Time:      7  15   30
Distance:  9  40  200
"""

def process(time, distance):
    print("race", time, distance)
    res = 0
    wait_time = 0
    while wait_time < time:
        wait_time += 1
        race_time = time - wait_time
        my_distance = wait_time * race_time
        if my_distance > distance:
            res += 1
            print("win", wait_time, my_distance)


    print()
    return res


def main(data):
    lines = data.split("\n")
    times, distances = re.findall("\d+", lines[0]), re.findall("\d+", lines[1])

    races = list(zip(times, distances))

    res = 1

    for race in races:
        time = int(race[0])
        distance = int(race[1])
        res *= process(time, distance)

    print("RES:", res)


if __name__ == "__main__":
    data = open("./input.txt", "r").read()
    main(data.strip())
