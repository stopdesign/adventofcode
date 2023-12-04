import re

data = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def card_points(card):
    head, body = card.split(":")
    nums = body.split("|")
    win_nums = re.findall("\d+", nums[0])
    my_nums = re.findall("\d+", nums[1])
    return len(set(win_nums) & set(my_nums))


def main(cards):
    cards_by_id = {}

    # create a dict with amount of points and a copy counter
    for i, card_str in enumerate(cards, 1):
        cards_by_id[i] = {"points": card_points(card_str), "copies": 1}

    for card_id, card in cards_by_id.items():
        # Points determines how many cards from the next N lines
        # will be copied once by each card copy on this line.
        # Add "1 * card.copies" for each affected card.
        for i in range(card["points"]):
            cards_by_id[card_id + i + 1]["copies"] += card["copies"]

    res = sum(v["copies"] for v in cards_by_id.values())
    print(res)


if __name__ == "__main__":
    data = open("./input_m.txt", "r").read()
    cards = data.strip().split("\n")
    main(cards)
