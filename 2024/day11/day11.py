import re
from collections import Counter
import time


def parse(filename: str) -> tuple[int, ...]:
    with open(filename) as f:
        nrs = tuple(map(int, re.findall(r"\d+", f.read().strip())))
    return nrs


def apply_rules(counter: Counter):
    counter_before = counter.copy()

    for stone_val, stone_count in counter_before.items():
        if stone_count == 0:
            continue

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
    counter = Counter(stones)

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


start_time = time.perf_counter()

# filename = "day11/example"
filename = "day11/input"

stones = parse(filename)
solve(stones)

end_time = time.perf_counter()
print(f"Total time: {end_time - start_time} seconds")
