import re
from time import monotonic


def parse_seed_ranges(data):
    res = []
    for pair in re.findall("\d+ \d+", data):
        seed_start, cnt = map(int, pair.split(" "))
        res.append((seed_start, seed_start + cnt))
    return res


def parse_map_rules(rules):
    res = []
    for rule in sorted(rules):
        dst_val, src_val, cnt = map(int, rule.split(" "))
        res.append((src_val, src_val + cnt - 1, dst_val - src_val))
    return tuple(res)


def parse_maps(data):
    res = []
    for block in data.split("\n\n"):
        head, body = block.strip().split(" map:")
        src, dst = head.split("-to-")
        rules = body.strip().split("\n")
        res.append(parse_map_rules(rules))
    return res


def location_to_seeds(value: int, maps) -> int:
    for rules in reversed(maps):
        for rule in rules:
            if rule[0] <= value - rule[2] <= rule[1]:
                value -= rule[2]
                break
        if value < 0:
            return -1
    return value


def calc(seed_ranges, maps):
    step = 10000

    for location in range(0, 100000000, step):
        seed = location_to_seeds(location, maps)

        valid_seed = any([r[0] <= seed <= r[1] for r in seed_ranges])
        if not valid_seed:
            continue

        # ok, we have a valid location-to-seed transformation here.
        # I assume the first block is started in the current loop step.

        for location_fine in range(location - step, location):
            seed = location_to_seeds(location_fine, maps)
            for lo_seed, hi_seed in seed_ranges:
                if lo_seed <= seed <= hi_seed:
                    print(location_fine)
                    return


def main(data):
    seeds_str, rules_str = data.split("\n", maxsplit=1)
    seed_pairs = parse_seed_ranges(seeds_str)
    maps = parse_maps(rules_str)
    calc(seed_pairs, maps)


if __name__ == "__main__":
    t1 = monotonic()
    path = "/".join(__file__.split("/")[:-1] + ["input.txt"])
    data = open(path).read()
    cards = data.strip()
    main(cards)
    print(f"Time: {monotonic() - t1:.4f} s")
