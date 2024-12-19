from functools import cache

filename = "day19/example"
# filename = "day19/input"


def parse(filename: str) -> tuple[set[str], list[str]]:
    with open(filename) as f:
        first, second = f.read().strip().split("\n\n")
        available = set(first.split(", "))
        designs = second.split("\n")

        return available, designs


@cache
def count_possible(design: str) -> int:
    if len(design) == 0:
        return 1
    else:
        count = 0
        for pattern in available_patterns:
            if design.startswith(pattern):
                count += count_possible(design[len(pattern) :])
    return count


def solve():
    is_possible_count = 0
    all_combinations_count = 0

    for design in designs:
        tmp = count_possible(design)
        if tmp > 0:
            is_possible_count += 1
            all_combinations_count += tmp

    assert is_possible_count == 338
    assert all_combinations_count == 841533074412361

    print("Part 1:", is_possible_count)
    print("Part 2:", all_combinations_count)


# filename = "day19/example"
filename = "day19/input"

available_patterns, designs = parse(filename)
solve()
