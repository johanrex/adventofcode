import sys
from enum import IntEnum


class Direction(IntEnum):
    LEFT = sys.maxsize - 1
    RIGHT = sys.maxsize - 2
    DOWN = sys.maxsize - 3


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


def can_move_in_direction(cave, pat, x_pat_left_src, y_pat_bottom_src, direction):
    x_offset = 0
    if direction == Direction.LEFT:
        x_offset = -1
        if x_pat_left_src <= 0:
            return False
    elif direction == Direction.RIGHT:
        x_offset = 1
        if x_pat_left_src + len(pat[0]) >= len(cave[0]):
            return False

    pat_height = len(pat)
    pat_width = len(pat[0])

    pat_y = 0
    for curr_y in range(y_pat_bottom_src - pat_height + 1, y_pat_bottom_src + 1):

        pat_x = 0
        for curr_x in range(x_pat_left_src + x_offset, x_pat_left_src + pat_width + x_offset):
            cave_val = cave[curr_y][curr_x]
            pat_val = pat[pat_y][pat_x]
            if cave_val == "#" and pat_val == "@":
                return False
            pat_x += 1
        pat_y += 1

    return True


def can_move_down(cave, pat, x_pat_left_src, y_pat_bottom_src):
    if y_pat_bottom_src - 1 == 0:
        return False


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

    pat_left_x = 2
    pat_bottom_y = pat_height - 1
    put_pattern_at(cave, pat, pat_left_x, pat_bottom_y)
    print_cave(cave)

    while can_move_in_direction(cave, pat, pat_left_x, pat_bottom_y, Direction.LEFT):
        remove_pattern_at(cave, pat, pat_left_x, pat_height - 1)
        pat_left_x -= 1
        put_pattern_at(cave, pat, pat_left_x, pat_bottom_y)
        print_cave(cave)

    while can_move_in_direction(cave, pat, pat_left_x, pat_bottom_y, Direction.RIGHT):
        remove_pattern_at(cave, pat, pat_left_x, pat_height - 1)
        pat_left_x += 1
        put_pattern_at(cave, pat, pat_left_x, pat_bottom_y)
        print_cave(cave)

    # Bottom left pos
    # pattern_pos =

    # is_at_rest()

    # "Each rock appears so that its left edge is two units away from the left wall and its bottom edge is three units above the highest rock in the room (or the floor, if there isn't one)."

    pat_idx = (pat_idx + 1) % len(patterns)
