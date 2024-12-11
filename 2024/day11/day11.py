from functools import cache
import math
import re
import copy
from collections import Counter


memo = dict()


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


def apply_rules_recursize(stones: tuple[int, ...]):
    if stones in memo:
        return memo[stones]

    if len(stones) == 1:
        stone = stones[0]

        if stone == 0:  # rule 1
            ans = (1,)
        elif len(str(stone)) % 2 == 0:  # rule 2
            stone = str(stone)
            middle = len(stone) // 2
            left = int(stone[:middle])
            right = int(stone[middle:])
            ans = left, right
        else:  # rule 3
            ans = (stone * 2024,)
    else:
        # split in half
        middle = len(stones) // 2
        left = stones[:middle]
        right = stones[middle:]
        ans = apply_rules_recursize(left) + apply_rules_recursize(right)

    memo[stones] = ans
    return ans


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


def part2(stones: tuple[int, ...]):
    print("Initial state:")
    print(stones)

    for i in range(75):
        stones = apply_rules_recursize(stones)
        print(f"After {i+1} blinks:", len(stones))

    ans = len(stones)
    print("Part 2:", ans)


# filename = "day11/example"
filename = "day11/input"

stones = parse(filename)
part1(stones)
part2(stones)
