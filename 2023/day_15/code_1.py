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

cnt = sum(hash(code) for code in codes)

print(cnt)
