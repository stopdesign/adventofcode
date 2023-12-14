import re
from time import monotonic

data = """ 
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def mask_to_binary(mask):
    hash_bin = mask.replace("#", "1").replace(".", "0").replace("?", "0")
    dot_bin = mask.replace("#", "0").replace(".", "1").replace("?", "0")
    return int(hash_bin, 2), int(dot_bin, 2)


def check_one_line(line):
    mask, nums = line.split()
    nums = [int(n) for n in nums.split(",")]
    nums_mask = ["1" * n for n in nums]
    h_mask, d_mask = mask_to_binary(mask)

    # compile regex for checking ### blocks sizes
    re_nums_mask = "0*"
    for i, n in enumerate(nums):
        re_nums_mask += "1" * n + "0+"
    re_nums_mask = re_nums_mask.strip("+") + "*"
    rx = re.compile(re_nums_mask)

    valid_cnt = 0
    for variant in range(2 ** len(mask)):
        if (
            (h_mask & variant) == h_mask  # check if all 1s are in place
            and (d_mask & variant) == 0  # check if all 0s are in place
            and rx.fullmatch(bin(variant)[2:])
        ):
            valid_cnt += 1

    # print(f"{mask:<25} {str(nums):<25} {valid_cnt}")

    return valid_cnt


def main(lines):
    res = sum(check_one_line(line) for line in lines)
    print(f"Result: {res}")


if __name__ == "__main__":
    t1 = monotonic()
    # data = open("day_12/input").read()
    data = data.strip().splitlines()
    main(data)
    print(f"Time: {monotonic() - t1:.4f} s")

#    #### # # ###
