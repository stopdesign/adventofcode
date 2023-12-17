from functools import lru_cache
from time import monotonic


def check_one_line(line, folding_factor=1):
    mask, nums = line.split()

    # unfold
    mask = "?".join([mask] * folding_factor)
    nums = ",".join([nums] * folding_factor)

    nums = tuple(int(n) for n in nums.split(","))

    return count_variants(mask, nums)


def can_use_block(mask, block_len):
    """
    Returns True if the beginning of the template
    is a valid block of given length plus a spacer.
    """
    block = "#" * block_len + "."
    can_cut = True
    for m, b in zip(mask, block):
        if not (m == "?" or m == b):
            can_cut = False
            break
    return can_cut


@lru_cache
def count_variants(mask, nums, block_idx=0):
    res = 0

    # Stop condition: no more blocks
    if block_idx >= len(nums):
        return int("#" not in mask)

    # Stop condition: no space for all blocks left
    if sum(nums[block_idx:]) > len(mask.replace(".", "")):
        return 0

    if can_use_block(mask, block_len=nums[block_idx]):
        # Cut the used template part, check the next block
        to_skip = nums[block_idx] + 1
        res += count_variants(mask[to_skip:], nums, block_idx + 1)

    # Skip the first template symbol if it could be .
    if len(mask) and mask[0] in ".?":
        res += count_variants(mask[1:], nums, block_idx)

    return res


def main(lines):
    folding_factor = 5
    res = sum(check_one_line(line, folding_factor) for line in lines)
    print(f"Result: {res}")


if __name__ == "__main__":
    t1 = monotonic()
    data = open("day_12/input").readlines()
    main(data)
    print(f"\nTime: {monotonic() - t1:.4f} s")
