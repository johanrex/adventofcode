import math
import re
import copy
from collections import Counter


def parse(filename: str):
    with open(filename) as f:
        nrs = list(map(int, re.findall(r"\d+", f.read().strip())))
    return nrs


def apply_rules(stones):
    i = 0
    while i < len(stones):
        stone = stones[i]

        if stone == 0:  # rule 1
            stones[i] = 1
        elif len(str(stone)) % 2 == 0:  # rule 2
            stone = str(stone)
            middle = len(stone) // 2
            left = int(stone[:middle])
            right = int(stone[middle:])
            stones[i] = left
            stones.insert(i + 1, right)

            # increment i since we inserted a new stone
            i += 1
        else:  # rule 3
            stones[i] = stone * 2024

        i += 1


def part1(stones):
    # print("Initial state:")
    # print(stones)
    for i in range(75):
        apply_rules(stones)

        print(f"After {i+1} blinks:", len(stones))

        # stones_str = list(map(str, stones))
        # print(" ".join(stones_str))
        # pass

    ans = len(stones)
    print("Part 1:", ans)


def part2(stones):
    print("Part 2:", -1)


# filename = "day11/example"
filename = "day11/input"

stones = parse(filename)
part1(stones)
part2(stones)
