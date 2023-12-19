from collections import defaultdict

data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def hash(text):
    res = 0
    for char in text:
        ascii_code = ord(char)
        res += ascii_code
        res *= 17
        res %= 256
    return res


data = open("day_15/input").read()
codes = data.strip().split(",")

boxes = defaultdict(dict)

for code in codes:
    if "-" in code:
        label = code.strip("-")
        box = hash(label)
        if label in boxes[box]:
            del boxes[box][label]
    else:
        label, num = code.split("=")
        box = hash(label)
        boxes[box][label] = int(num)

res = 0
for box, lenses in boxes.items():
    for lens_num, focal in enumerate(lenses.values(), 1):
        res += (1 + box) * lens_num * focal

print(res)
#
