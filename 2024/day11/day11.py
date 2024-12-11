from functools import cache
import math
import re
import copy
from collections import Counter

counter = Counter()


def parse(filename: str) -> tuple[int, ...]:
    with open(filename) as f:
        nrs = tuple(map(int, re.findall(r"\d+", f.read().strip())))
    return nrs


def apply_rules_p1(stones: tuple[int, ...]):
    new_stones = []
    i = 0
    while i < len(stones):
        stone = stones[i]

        if stone == 0:  # rule 1
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:  # rule 2
            stone = str(stone)
            middle = len(stone) // 2
            left = int(stone[:middle])
            right = int(stone[middle:])
            new_stones.append(left)
            new_stones.append(right)
        else:  # rule 3
            new_stones.append(stone * 2024)

        i += 1
    return tuple(new_stones)


def part1(stones: tuple[int, ...]):
    print("Initial state:")
    print(stones)
    for i in range(25):
        stones = apply_rules_p1(stones)

        # print(f"After {i+1} blinks:", len(stones))

        # print(" ".join(stones_str))
        # pass

    ans = len(stones)
    print("Part 1:", ans)


def apply_rules_p2(counter: Counter):
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


def part2(stones: tuple[int, ...]):
    print("Initial state:")
    print(stones)
    for stone in stones:
        counter[stone] += 1

    for i in range(75):
        apply_rules_p2(counter)

    ans = sum(counter.values())
    assert ans == 257246536026785
    print("Part 2:", ans)


# filename = "day11/example"
filename = "day11/input"

stones = parse(filename)
part1(stones)
part2(stones)
