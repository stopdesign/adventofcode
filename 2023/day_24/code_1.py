from itertools import combinations

from shapely import LineString, Point, intersects

data = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


def path_segment_within_borders(p, v, border_min, border_max):
    """
    Find any future (t > 0) intersection with borders.
    If the point was outside - use 2 intersection points.
    """
    intersections = []

    if v.y != 0:
        t_top = (border_max - p.y) / v.y
        if t_top > 0:
            x_top = p.x + v.x * t_top
            if border_min <= x_top <= border_max:
                i_top = Point(x_top, border_max)
                intersections.append((t_top, i_top))

        t_bottom = (border_min - p.y) / v.y
        if t_bottom > 0:
            x_bottom = p.x + v.x * t_bottom
            if border_min <= x_bottom <= border_max:
                i_bottom = Point(x_bottom, border_min)
                intersections.append((t_bottom, i_bottom))

    if v.x != 0:
        t_left = (border_min - p.x) / v.x
        if t_left > 0:
            y_left = p.y + v.y * t_left
            if border_min <= y_left <= border_max:
                i_left = Point(border_min, y_left)
                intersections.append((t_left, i_left))

        t_right = (border_max - p.x) / v.x
        if t_right > 0:
            y_right = p.y + v.y * t_right
            if border_min <= y_right <= border_max:
                i_right = Point(border_max, y_right)
                intersections.append((t_right, i_right))

    intersections = sorted(intersections)

    assert len(intersections) in [1, 2]

    if border_min <= p.x <= border_max and border_min <= p.y <= border_max:
        return p, intersections[0][1]
    else:
        # the starting point was outside of the box
        # use both intersection points as a segment
        return intersections[0][1], intersections[1][1]


def main(data):
    hails = []

    # X and Y coordinates of the border
    border_min = 7
    border_max = 27
    if len(data) > 1000:
        border_min = 200000000000000
        border_max = 400000000000000

    for line in data.splitlines():
        pos, speed = line.replace(" ", "").split("@")
        px, py, pz = map(float, pos.split(","))
        vx, vy, vz = map(float, speed.split(","))

        p = Point(px, py)
        v = Point(vx, vy)

        segment = path_segment_within_borders(p, v, border_min, border_max)
        hails.append(segment)

    res = 0
    for a, b in combinations(hails, 2):
        res += int(intersects(LineString(a), LineString(b)))

    print("res:", res)


if __name__ == "__main__":
    data = open("day_24/input").read()
    main(data.strip())
#
