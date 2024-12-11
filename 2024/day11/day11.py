import re
import copy
from collections import Counter

counter = Counter()


def parse(filename: str) -> tuple[int, ...]:
    with open(filename) as f:
        nrs = tuple(map(int, re.findall(r"\d+", f.read().strip())))
    return nrs


def apply_rules(counter: Counter):
    counter_before = copy.deepcopy(counter)

    actual_stone_vals = [k for k, v in counter.items() if v > 0]
    for stone_val in actual_stone_vals:
        stone_count = counter_before[stone_val]
        counter[stone_val] -= stone_count
        if counter[stone_val] < 0:
            counter[stone_val] = 0

        if stone_val == 0:  # rule 1
            counter[1] += stone_count
        elif len(str(stone_val)) % 2 == 0:  # rule 2
            stone_val = str(stone_val)
            middle = len(stone_val) // 2
            left = int(stone_val[:middle])
            right = int(stone_val[middle:])

            counter[left] += stone_count
            counter[right] += stone_count
        else:  # rule 3
            counter[stone_val * 2024] += stone_count


def solve(stones: tuple[int, ...]):
    # initialize counter with stones
    for stone in stones:
        counter[stone] += 1

    for i in range(75):
        apply_rules(counter)
        if i == 24:
            p1 = sum(counter.values())
            assert p1 == 217443
            print("Part 1:", p1)

        if i == 74:
            p2 = sum(counter.values())
            assert p2 == 257246536026785
            print("Part 2:", p2)


# filename = "day11/example"
filename = "day11/input"

stones = parse(filename)
solve(stones)
