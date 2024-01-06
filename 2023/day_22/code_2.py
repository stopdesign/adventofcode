from collections import defaultdict

import networkx as nx

data = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


class Block:
    idx: int
    grid_size: int

    def __init__(self, raw, grid_size, idx):
        """
        Parsing
        """
        self.idx = idx
        aa, bb = raw.split("~")
        aa = [int(a) for a in aa.split(",")]
        bb = [int(b) for b in bb.split(",")]
        self.grid_size = grid_size
        self.vol = [abs(a - b) + 1 for a, b in zip(aa, bb)]
        self.pos = min(aa[0], bb[0]), min(aa[1], bb[1])
        self.top_initial = max(aa[2], bb[2])
        self.top = 0
        self.profile = self.get_profile()

    def __repr__(self):
        p = ("".join(map(str, self.profile))).replace("0", ".")
        return f"{self.idx}, {self.vol}, pos: {self.pos}, top: {self.top}, p: {p}"

    def get_profile(self):
        """
        Thickness for each column (z coordinate).
        """
        res = [0] * self.grid_size**2
        for y in range(self.pos[1], self.pos[1] + self.vol[1]):
            for x in range(self.pos[0], self.pos[0] + self.vol[0]):
                res[y * self.grid_size + x] = self.vol[2]
        return res


def settle_blocks(blocks, size, tower, top_block):
    """
    Put all the blocks into their places,
    calculate the load for each block.
    """
    load_by_block = defaultdict(list)

    # Stackenblochen!
    for block in blocks:
        # where the top will settle after the fall
        for i in range(size):
            if not block.profile[i]:
                continue
            block.top = max(block.top, tower[i] + block.profile[i])
        for i in range(size):
            if not block.profile[i]:
                continue
            # if equal than block touches the prev
            # top block in this column (supported by it)
            if tower[i] == block.top - block.profile[i]:
                load_by_block[top_block[i]].append(block.idx)
            tower[i] = block.top
            top_block[i] = block.idx
    return load_by_block


def main(data):
    if len(data) < 1000:
        grid_size = 3
    else:
        grid_size = 10

    blocks = [Block(raw, grid_size, i) for i, raw in enumerate(data.splitlines(), 1)]

    # sort blocks by initial altitude to prevent
    # blocking some initial positions by fallen blocks
    blocks = sorted(blocks, key=lambda b: b.top_initial)

    size = grid_size**2

    # Better with one coordinate instead of x-y matrix
    tower = [0] * size
    top_block = [0] * size

    load_by_block = settle_blocks(blocks, size, tower, top_block)

    # for block, load in reversed(load_by_block.items()):
    #     print(block, load)

    gnx = nx.DiGraph(load_by_block)
    print(gnx)

    blocks_without_support_cnt = 0

    # try every node except the ground
    for node in filter(None, gnx):
        node_edges = list(gnx.edges(node))

        # disconnect this node
        gnx.remove_edges_from(node_edges)

        # count nodes disconnected from the ground
        still_connected_cnt = len(nx.descendants(gnx, 0))
        blocks_without_support_cnt += len(blocks) - still_connected_cnt

        # connect node back
        gnx.add_edges_from(node_edges)

    print("\nres", blocks_without_support_cnt)


if __name__ == "__main__":
    data = open("day_22/input").read()
    main(data.strip())
#
