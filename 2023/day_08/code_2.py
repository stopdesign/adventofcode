import math
import re
from dataclasses import dataclass
from functools import reduce

data = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


@dataclass
class Node:
    value: str
    left: str
    right: str

    @classmethod
    def from_str(cls, s) -> "Node":
        value, left, right = re.findall(r"[0-9A-Z]{3}", s)
        return cls(value, left, right)


def parse_nodes(lines):
    res = {}
    for line in lines:
        node = Node.from_str(line)
        res[node.value] = node
    return res


def lcm(a, b):
    return a * b // math.gcd(a, b)


def path_lengths(start_values, nodes, path):
    """
    Find num_steps for each start position
    """
    steps = []
    for val in start_values:
        cur_node = nodes[val]
        step = 0
        while not cur_node.value.endswith("Z"):
            turn = path[step % len(path)]
            destination = cur_node.right if turn == "R" else cur_node.left
            cur_node = nodes[destination]
            step += 1
        steps.append(step)
    return steps


def main(data):
    lines = list(filter(None, data.strip().split("\n")))

    path = lines.pop(0).strip()
    nodes = parse_nodes(lines)

    start_values = list(filter(lambda v: v.endswith("A"), nodes.keys()))
    print(start_values)

    lengths = path_lengths(start_values, nodes, path)

    print(lengths)
    res = reduce(lcm, lengths)

    print("Res:", res)


if __name__ == "__main__":
    data = open("./day_08/input.txt", "r").read()
    main(data)
