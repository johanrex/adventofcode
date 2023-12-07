from collections import Counter
from dataclasses import dataclass
from functools import cmp_to_key

# types of hands
FIVE_OF_A_KIND = 700
FOUR_OF_A_KIND = 600
FULL_HOUSE = 500
THREE_OF_A_KIND = 400
TWO_PAIRS = 300
ONE_PAIR = 200
HIGH_CARD = 100


CARD_VALUE_MAPPER = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,  # change since part 1
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


@dataclass
class HandInfo:
    hand: str
    bid: int


def parse(filename):
    hand_infos = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            parts = line.split()
            hand = parts[0]
            bid = int(parts[1])

            h = HandInfo(hand=hand, bid=bid)
            hand_infos.append(h)

    return hand_infos


def get_hand_type(hand):
    c = Counter(hand)

    if "J" in c:
        if c["J"] < 5:
            lst = c.most_common()
            cards_without_j = [x[0] for x in lst if x[0] != "J"]
            most_common_not_j = cards_without_j[0]
            c[most_common_not_j] += c["J"]
            del c["J"]

    freq = sorted(list(c.values()), reverse=True)

    if freq[0] == 5:
        type = FIVE_OF_A_KIND
    elif freq[0] == 4:
        type = FOUR_OF_A_KIND
    elif freq[0] == 3 and freq[1] == 2:
        type = FULL_HOUSE
    elif freq[0] == 3:
        type = THREE_OF_A_KIND
    elif freq[0] == 2 and freq[1] == 2:
        type = TWO_PAIRS
    elif freq[0] == 2:
        type = ONE_PAIR
    else:
        type = HIGH_CARD

    return type


def compare_hand(h1, h2):
    # Custom compare function
    # Return negative if x < y, zero if x == y, positive if x > y.

    t1 = get_hand_type(h1)
    t2 = get_hand_type(h2)

    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    else:
        for i in range(len(h1)):
            if h1[i] != h2[i]:
                if CARD_VALUE_MAPPER[h1[i]] < CARD_VALUE_MAPPER[h2[i]]:
                    return -1
                elif CARD_VALUE_MAPPER[h1[i]] > CARD_VALUE_MAPPER[h2[i]]:
                    return 1
    return 0


def compare_hand_info(hi1, hi2):
    return compare_hand(hi1.hand, hi2.hand)


def part2(hand_infos):
    hand_infos_sorted = sorted(hand_infos, key=cmp_to_key(compare_hand_info))

    total_winning = 0
    for rank, hi in enumerate(hand_infos_sorted, 1):
        winning = rank * hi.bid
        total_winning += winning

    print("Part 2:", total_winning)


# filename = "7/example"
filename = "7/input"

hand_infos = parse(filename)

part2(hand_infos)
