import re
from dataclasses import dataclass

data = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""


@dataclass
class Node:
    value: str
    left: str
    right: str

    @classmethod
    def from_str(cls, s) -> "Node":
        value, left, right = re.findall(r"[A-Z]{3}", s)
        return cls(value, left, right)


def parse_nodes(lines):
    res = {}
    for line in lines:
        node = Node.from_str(line)
        res[node.value] = node
    return res


def main(data):
    lines = list(filter(None, data.strip().split("\n")))

    path = lines.pop(0)
    nodes = parse_nodes(lines)

    step = 0
    cur_node = nodes["AAA"]

    while cur_node.value != "ZZZ":
        turn = path[step % len(path)]
        destination = cur_node.right if turn == "R" else cur_node.left

        # prevent endless loop
        assert cur_node != destination

        cur_node = nodes[destination]
        step += 1

        print(step, turn, cur_node.value)

    print("Res:", step)


if __name__ == "__main__":
    path = "/".join(__file__.split("/")[:-1] + ["input.txt"])
    data = open(path).read()
    main(data)


