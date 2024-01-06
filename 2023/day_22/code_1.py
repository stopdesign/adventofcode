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
    raw: str
    grid_size: int

    def __init__(self, raw, grid_size):
        self.raw = raw
        aa, bb = raw.split("~")
        aa = [int(a) for a in aa.split(",")]
        bb = [int(b) for b in bb.split(",")]
        self.grid_size = grid_size
        self.vol = [abs(a - b) + 1 for a, b in zip(aa, bb)]
        self.pos = min(aa[0], bb[0]), min(aa[1], bb[1])
        self.top_initial = max(aa[2], bb[2])
        self.top = 0
        self.profile = self.get_profile()
        self.supported_by = set()

    def __repr__(self):
        p = ("".join(map(str, self.profile))).replace("0", ".")
        return f"{self.raw:>15} - {self.vol}, pos: {self.pos}, top: {self.top}, p: {p}"

    def get_profile(self):
        """
        Thickness for each column (z coordinate)
        """
        res = [0] * self.grid_size**2
        for y in range(self.pos[1], self.pos[1] + self.vol[1]):
            for x in range(self.pos[0], self.pos[0] + self.vol[0]):
                # print(self.pos, self.vol)
                res[y * self.grid_size + x] = self.vol[2]
        return res


def main(data):
    if len(data) < 1000:
        grid_size = 3
    else:
        grid_size = 10

    blocks = [Block(raw, grid_size) for raw in data.splitlines()]

    # sort blocks by initial altitude
    blocks = list(sorted(blocks, key=lambda b: b.top_initial))

    # for block in blocks[::-1]:
    #     print(block)

    size = grid_size**2
    tower = [0] * size
    top_block = [None] * size

    main_supports = {}

    # Stackenblochen!
    for block in blocks:
        # where the top will settle after the fall
        top = max(tower[i] + block.profile[i] for i in range(size) if block.profile[i])
        block.top = top
        for i in range(size):
            if block.profile[i]:
                # if equal than block touches the prev top block (supported by it)
                if tower[i] == block.top - block.profile[i]:
                    block.supported_by.add(top_block[i])
                tower[i] = top
                top_block[i] = str(block.raw)
        if len(block.supported_by) == 1:
            main_support = list(block.supported_by)[0]
            if main_support:
                main_supports[main_support] = block.raw

    a = len(blocks)
    b = len(main_supports)

    print(f"blocks: {a} \nexclusive supports: {b} \nremovable: {a-b}\n")


if __name__ == "__main__":
    data = open("day_22/input").read()
    main(data.strip())
#
