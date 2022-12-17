def print_cave(cave):
    print("This is the cave:")
    for lst in cave:
        print("".join(lst))


def print_pattern(pat):
    for line in pat:
        print(line)


def count_empty_lines_from_top(cave):
    count = 0
    for line in cave:
        if line == ["."] * 7:
            count += 1
        else:
            break
    return count


def extend_cave(cave, l):
    for _ in range(l):
        cave.insert(0, ["."] * 7)


def remove_pattern_at(cave, pat, x_left, y_bottom):
    pat_height = len(pat)
    pat_width = len(pat[0])
    pat_y = 0
    for curr_y in range(y_bottom - pat_height + 1, y_bottom + 1):
        pat_x = 0
        for curr_x in range(x_left, x_left + pat_width):
            if pat[pat_y][pat_x] != ".":
                cave[curr_y][curr_x] = "."
            pat_x += 1
        pat_y += 1


def put_pattern_at(cave, pat, x_left, y_bottom):
    pat_height = len(pat)
    pat_width = len(pat[0])

    pat_y = 0
    for curr_y in range(y_bottom - pat_height + 1, y_bottom + 1):
        pat_x = 0
        for curr_x in range(x_left, x_left + pat_width):
            cave[curr_y][curr_x] = pat[pat_y][pat_x]
            pat_x += 1
        pat_y += 1


filename = "17/example"
with open(filename) as f:
    jet = list(f.read().strip())

patterns = [
    [[*"@@@@"]],
    [[*".@."], [*"@@@"], [*".@."]],
    [[*"..@"], [*"..@"], [*"@@@"]],
    [[*"@"], [*"@"], [*"@"], [*"@"]],
    [[*"@@"], [*"@@"]],
]

cave: list[list[str]] = []
pat_idx = 0
jet_idx = 0

# for pat in patterns:
#     print_pattern(pat)

# extend_cave(cave, 3)
# print_cave(cave)
# print(count_empty_lines_from_top(cave))

for i in range(1):
    empty_lines = count_empty_lines_from_top(cave)
    lines_to_extend = 3 - empty_lines
    assert lines_to_extend >= 0
    extend_cave(cave, lines_to_extend)

    pat = patterns[pat_idx]
    pat_height = len(pat)
    extend_cave(cave, pat_height)

    put_pattern_at(cave, pat, 1, pat_height - 1)
    print_cave(cave)

    remove_pattern_at(cave, pat, 1, pat_height - 1)
    print_cave(cave)

    pat = patterns[1]
    pat_height = len(pat)
    put_pattern_at(cave, pat, 1, pat_height - 1)
    print_cave(cave)

    remove_pattern_at(cave, pat, 1, pat_height - 1)
    print_cave(cave)

    # Bottom left pos
    # pattern_pos =

    # is_at_rest()

    # "Each rock appears so that its left edge is two units away from the left wall and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one)."

    pat_idx = (pat_idx + 1) % len(patterns)
