import re

data = """ 
Time:      7  15   30
Distance:  9  40  200
"""

def process(time, distance):
    res = 0
    wait_time = 1
    while wait_time < time:
        my_distance = wait_time * (time - wait_time)
        if my_distance > distance:
            res += 1
        wait_time += 1
    return res


def main(data):
    lines = data.split("\n")
    times, distances = re.findall("\d+", lines[0]), re.findall("\d+", lines[1])

    time = int("".join(times))
    distance = int("".join(distances))

    res = process(time, distance)

    # races = list(zip(times, distances))

    # for race in races:
        # time = int(race[0])
        # distance = int(race[1])
        # res *= process(time, distance)

    print("RES:", res)


if __name__ == "__main__":
    data = open("./input.txt", "r").read()
    main(data.strip())
