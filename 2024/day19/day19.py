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
def is_possible(design: str) -> bool:
    if len(design) == 0:
        return True
    else:
        for pattern in available_patterns:
            if design.startswith(pattern) and is_possible(design[len(pattern) :]):
                return True
    return False


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
    all_possible_count = 0

    for design in designs:
        if is_possible(design):
            is_possible_count += 1

        all_possible_count += count_possible(design)

    assert is_possible_count == 338
    assert all_possible_count == 841533074412361

    print("Part 1:", is_possible_count)
    print("Part 2:", all_possible_count)


# filename = "day19/example"
filename = "day19/input"

available_patterns, designs = parse(filename)
solve()
