def parse(filename) -> tuple[list[tuple[int, int]], list[int]]:
    ranges = []
    ingredients = []
    with open(filename) as f:
        first_part = True
        while line := f.readline():
            line = line.strip()

            if len(line) == 0:
                first_part = False
                continue

            if first_part:
                # ranges
                start, end = line.split("-")
                ranges.append((int(start), int(end)))
            else:
                # ingredients
                ingredients.append(int(line))
    return ranges, ingredients


# this is the same as leetcode 56. merge intervals: https://leetcode.com/problems/merge-intervals/description/
def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # sort input on start
    ranges.sort()

    ans = []

    for range in ranges:
        if len(ans) == 0:
            ans.append(range)
        else:
            _, prev_end = ans[-1]

            curr_start, curr_end = range

            # start new range
            if curr_start > prev_end:
                ans.append(range)

            # extend prev range
            else:
                if curr_end > prev_end:
                    last_range = ans[-1]
                    start, _ = last_range
                    ans[-1] = (start, curr_end)

    return ans


def part1(ranges: list[tuple[int, int]], ingredients: list[int]):
    fresh_cnt = 0

    for ingredient in ingredients:
        for start, end in ranges:
            if start <= ingredient <= end:
                fresh_cnt += 1
                break

    print("Part 1:", fresh_cnt)


def part2(ranges: list[tuple[int, int]]):
    ranges = merge_ranges(ranges)

    total_span = 0
    for start, end in ranges:
        total_span += end - start + 1

    print("Part 2:", total_span)


filename = "day05/example"
filename = "day05/input"

ranges, ingredients = parse(filename)

part1(ranges, ingredients)
part2(ranges)
