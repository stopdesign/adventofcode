data = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


class Map:
    def __init__(self, src, dst, rules):
        self.src = src
        self.dst = dst
        self._map = {}
        self._rules = []
        self.parse_rules(rules)

    def parse_rules(self, rules):
        for rule in rules:
            dst_val, src_val, cnt = map(int, rule.split(" "))
            self._rules.append(
                {
                    "start": src_val,
                    "end": src_val + cnt - 1,
                    "shift": dst_val - src_val,
                }
            )

    def convert(self, val):
        for rule in self._rules:
            if rule["start"] <= val <= rule["end"]:
                return val + rule["shift"]
        return val


def parse_seeds(data):
    return list(map(int, data.split(":")[1].strip().split(" ")))


def parse_maps(data):
    maps_by_src = {}
    blocks = data.split("\n\n")
    for block in blocks:
        head, body = block.strip().split(" map:")
        src, dst = head.split("-to-")
        rules = body.strip().split("\n")
        maps_by_src[src] = Map(src, dst, rules)
    return maps_by_src


def main(data):
    seeds_str, maps_str = data.split("\n", maxsplit=1)
    seeds = parse_seeds(seeds_str)
    maps = parse_maps(maps_str)

    cur_src = "seed"
    locations = []

    for seed in seeds:
        print("seed", seed)
        cur_val = seed
        cur_src = "seed"
        while cur_src != "location":
            map = maps[cur_src]
            cur_val = map.convert(cur_val)
            cur_src = map.dst
        locations.append(cur_val)

    print(min(locations))


if __name__ == "__main__":
    path = "/".join(__file__.split("/")[:-1] + ["input.txt"])
    data = open(path).read()
    cards = data.strip()
    main(cards)
