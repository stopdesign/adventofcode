import re
from time import monotonic
from code_1 import check_one_line as chl 

data = "\n".join(
    [
        "???.### 1,1,3",
        ".??..??...?##. 1,1,3",
        "?#?#?#?#?#?#?#? 1,3,1,6",
        "????.#...#... 4,1,1",
        "????.######..#####. 1,6,5",
        "?###???????? 3,2,1",
    ]
)


def mask_to_binary(mask):
    hash_bin = mask.replace("#", "1").replace(".", "0").replace("?", "0")
    dot_bin = mask.replace("#", "0").replace(".", "1").replace("?", "0")
    return int(hash_bin, 2), int(dot_bin, 2)


def compile_regex(nums):
    """Compile regex for checking ### blocks sizes"""
    re_nums_mask = "0*"
    for i, n in enumerate(nums):
        re_nums_mask += "1" * n + "0+"
    re_nums_mask = re_nums_mask.strip("+") + "*"
    return re.compile(re_nums_mask)


def show_bits(nums):
    print()
    for n in nums:
        print(f"{n:>3} {bin(n)[2:]:>10}")
    print()


def check_variant(nums_mask, h_mask, d_mask):
    variant = sum(nums_mask)
    # print(f"{str(nums_mask):<25} {bin(variant)[2:]:>25}")
    return (h_mask & variant) == h_mask and (d_mask & variant) == 0


def check_one_line(line):
    mask, nums = line.split()

    h_mask, d_mask = mask_to_binary(mask)

    nums = [int(n) for n in nums.split(",")]
    nums_mask = ["1" * n for n in nums]
    nums_mask = list(map(lambda x: int(x, 2), nums_mask))
    # rx = compile_regex(nums)

    max_value = 2 ** len(mask) - 1

    # print("\n")
    # print(nums)
    # print(nums_mask)

    # shift bits
    cum_shift = 0
    for i in range(len(nums_mask) - 1, -1, -1):
        nums_mask[i] <<= cum_shift
        cum_shift += nums[i] + 1  # save space for 0s

    min_variant = sum(nums_mask)

    # nums_mask is in the initial state now
    # show_bits(nums_mask)

    shift_all_way_left = len(mask) - len(f"{min_variant:b}")
    for i in range(len(nums_mask)):
        nums_mask[i] <<= shift_all_way_left

    variant = sum(nums_mask)
    max_variant = sum(nums_mask)

    print(f"{mask:<25} {variant:>25b}  {variant}")
    # print(f"{max_value:<25b} {max_value:>25b} {max_value}")
    # print(f"{min_variant:<25b} {min_variant:>25b} {min_variant}")
    # print(f"{max_variant:<25b} {max_variant:>25b} {max_variant}")
    # print()

    variants = process_number(nums, nums_mask, 0, h_mask, d_mask)
    if check_variant(nums_mask, h_mask, d_mask):
        variants += 1
    # old_vars = chl(line)
    # print(f"variants: {variants}, old_vars: {old_vars}")

    # if variants != old_vars:
        # print("ERROR")
        # exit()

    return variants


def process_number(nums, nums_mask, start, h_mask, d_mask):

    res = 0

    if start >= len(nums_mask):
        return res

    nums_mask = list(nums_mask)

    res += process_number(nums, nums_mask, start + 1, h_mask, d_mask)

    for i in range(start, len(nums_mask)):
        nums_mask[i] >>= 1

    possible = True
    for i in range(len(nums_mask)):
        if nums_mask[i] < 2 ** nums[i] - 1:
            possible = False
            return res
            # break

    if possible and all(nums_mask):
        if check_variant(nums_mask, h_mask, d_mask):
            # print(f"{str(nums_mask):<25} {bin(sum(nums_mask))[2:]:>25}  {start}")
            res += 1
            # res.append(sum(nums_mask))
 
    if possible:
        res += process_number(nums, nums_mask, start, h_mask, d_mask)

    return res 


def main(lines):
    res = sum(check_one_line(line) for line in lines)
    print(f"\nResult: {res}")


if __name__ == "__main__":
    t1 = monotonic()
    data = open("day_12/input").read()
    data = data.strip().splitlines()
    main(data)
    print(f"\nTime: {monotonic() - t1:.4f} s")

#    #### # # ###
