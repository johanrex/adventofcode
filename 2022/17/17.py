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


# cave is assumed to be empty where pat should be placed.
def put_pattern_at(cave, pat, x_left, y_bottom, chr="@"):
    pat_height = len(pat)
    pat_width = len(pat[0])

    pat_y = 0
    for curr_y in range(y_bottom - pat_height + 1, y_bottom + 1):
        pat_x = 0
        for curr_x in range(x_left, x_left + pat_width):
            if pat[pat_y][pat_x] != ".":
                assert cave[curr_y][curr_x] == "."  # TODO remove for performance
                cave[curr_y][curr_x] = chr
            pat_x += 1
        pat_y += 1


def can_move_in_direction(cave, pat, x_pat_left_src, y_pat_bottom_src, direction):
    x_offset = 0
    y_offset = 0
    if direction == Direction.LEFT:
        x_offset = -1
        if x_pat_left_src <= 0:
            return False
    elif direction == Direction.RIGHT:
        x_offset = 1
        if x_pat_left_src + len(pat[0]) >= len(cave[0]):
            return False
    elif direction == Direction.DOWN:
        y_offset = 1
        if y_pat_bottom_src + 1 >= len(cave):
            return False

    pat_height = len(pat)
    pat_width = len(pat[0])

    pat_y = 0
    for curr_y in range(y_pat_bottom_src + y_offset - pat_height + 1, y_pat_bottom_src + 1 + y_offset):

        pat_x = 0
        for curr_x in range(x_pat_left_src + x_offset, x_pat_left_src + pat_width + x_offset):
            cave_val = cave[curr_y][curr_x]
            pat_val = pat[pat_y][pat_x]
            if cave_val == "#" and pat_val == "@":
                return False
            pat_x += 1
        pat_y += 1

    return True


def drop_rocks(filename, nr_of_rocks):
    with open(filename) as f:
        jets = list(f.read().strip())

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

    for rock_idx in range(nr_of_rocks):
        pat = patterns[pat_idx]
        pat_height = len(pat)
        needed_lines = pat_height + 3
        empty_lines = count_empty_lines_from_top(cave)

        if needed_lines > empty_lines:
            lines_to_extend = needed_lines - empty_lines
            extend_cave(cave, lines_to_extend)
            empty_lines = empty_lines + lines_to_extend
            assert lines_to_extend <= 6

        pat_left_x = 2
        # pat_bottom_y = pat_height - 1
        pat_bottom_y = empty_lines - 3 - 1

        put_pattern_at(cave, pat, pat_left_x, pat_bottom_y)
        if (rock_idx + 1) % 10_000 == 0:
            print(f"Rock {rock_idx+1} spawned.")

        # print(f"Rock {rock_idx+1} spawned.")
        # print_cave(cave)

        is_falling = True
        while is_falling:

            jet = jets[jet_idx]

            if jet == ">":
                direction = Direction.RIGHT
                x_offset = 1
            else:
                direction = Direction.LEFT
                x_offset = -1

            if can_move_in_direction(cave, pat, pat_left_x, pat_bottom_y, direction):
                remove_pattern_at(cave, pat, pat_left_x, pat_bottom_y)
                pat_left_x += x_offset
                put_pattern_at(cave, pat, pat_left_x, pat_bottom_y)

            if can_move_in_direction(cave, pat, pat_left_x, pat_bottom_y, Direction.DOWN):
                remove_pattern_at(cave, pat, pat_left_x, pat_bottom_y)
                pat_bottom_y += 1
                put_pattern_at(cave, pat, pat_left_x, pat_bottom_y)
            else:
                is_falling = False
                remove_pattern_at(cave, pat, pat_left_x, pat_bottom_y)
                put_pattern_at(cave, pat, pat_left_x, pat_bottom_y, chr="#")

            # print_cave(cave)

            jet_idx = (jet_idx + 1) % len(jets)
        pat_idx = (pat_idx + 1) % len(patterns)

    return len(cave) - count_empty_lines_from_top(cave)


filename = "17/input"
# filename = "17/example"

p1 = drop_rocks(filename, 2022)
assert p1 == 3171
print("Part1:", p1)


p2 = drop_rocks(filename, 1000000000000)
print("Part2:", p2)
