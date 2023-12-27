import re
from time import monotonic

import numpy as np


def parse_map_rules(rules):
    res = []
    for rule in sorted(rules):
        dst_val, src_val, cnt = map(int, rule.split(" "))
        res.append((src_val, src_val + cnt - 1, dst_val - src_val))
    return tuple(res)


def parse_seed_ranges(data):
    res = []
    for pair in re.findall("\d+ \d+", data):
        seed_start, cnt = map(int, pair.split(" "))
        res.append((seed_start, seed_start + cnt))
    return res


def parse_maps(data):
    res = []
    for block in data.split("\n\n"):
        head, body = block.strip().split(" map:")
        src, dst = head.split("-to-")
        rules = body.strip().split("\n")
        res.append(parse_map_rules(rules))
    return res


def backtrace_locations_to_seeds(maps, i, cnt):
    # a batch of seeds to test
    a = np.arange(i, i + cnt - 1, dtype=np.int64)

    # apply all rules
    for rules in reversed(maps):
        conditions = [
            np.logical_and(a - shft >= s, a - shft <= e) for s, e, shft in rules
        ]
        shifts = [rule[2] for rule in rules]
        a -= np.select(conditions, shifts)

    return a


def find_min_location(seeds, maps):
    if seeds.size == 0:
        return seeds

    # apply all rules
    for rules in maps:
        conditions = [np.logical_and(seeds >= s, seeds <= e) for s, e, _ in rules]
        shifts = [rule[2] for rule in rules]
        seeds += np.select(conditions, shifts)

    return np.amin(seeds)


def calc(seed_ranges, maps):
    batch_size = 100000
    max_location = 100000000

    for i in range(0, max_location, batch_size):
        seeds = backtrace_locations_to_seeds(maps, i, batch_size)

        for sr in seed_ranges:
            if_valid = (seeds >= sr[0]) & (seeds <= sr[1])
            min_location = find_min_location(seeds[if_valid], maps)
            if min_location.size > 0:
                return min_location


def main(data):
    seeds_str, maps_str = data.split("\n", maxsplit=1)
    seed_ranges = parse_seed_ranges(seeds_str)
    maps = parse_maps(maps_str)
    res = calc(seed_ranges, maps)
    print(res)


if __name__ == "__main__":
    t1 = monotonic()
    path = "/".join(__file__.split("/")[:-1] + ["input.txt"])
    data = open(path).read()
    cards = data.strip()
    main(cards)
    print(f"Time: {monotonic() - t1:.4f} s")
