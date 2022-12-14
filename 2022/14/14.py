import bisect

"""
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def print_current(blocked, sands):
    min_x = blocked[0][0]
    max_x = blocked[-1][0]

    y_blocked = list(sorted(blocked, key=lambda coord: coord[1]))
    # min_y = y_blocked[0][1]
    min_y = 0
    max_y = y_blocked[-1][1]

    x_count = (max_x + 1) - (min_x - 1)
    y_count = (max_y + 1) - min_y

    lines = []
    for _ in range(y_count):
        lines.append(["."] * x_count)

    lines[0][500 - min_x + 1] = "+"

    for x, y in blocked:
        norm_y = y - min_y
        norm_x = x - min_x + 1
        lines[norm_y][norm_x] = "#"

    for x, y in sands:
        norm_y = y - min_y
        norm_x = x - min_x + 1
        lines[norm_y][norm_x] = "o"

    for i, line in enumerate(lines):
        print(i, " ", "".join(line))


def parse_input(filename):
    blocked = []

    with open(filename) as f:
        prev_x = prev_y = None
        for line in f:
            # print("Parsing line: ", line)
            coords = line.strip().split(" -> ")

            for i in range(1, len(coords)):

                prev_x, prev_y = list(map(int, list(coords[i - 1].split(","))))
                curr_x, curr_y = list(map(int, list(coords[i].split(","))))

                from_x, to_x = list(sorted([prev_x, curr_x]))
                from_y, to_y = list(sorted([prev_y, curr_y]))

                if from_y == to_y:
                    for i_x in range(from_x, to_x + 1):
                        blocked_coord = (i_x, curr_y)
                        bisect.insort(blocked, blocked_coord)
                elif from_x == to_x:
                    for i_y in range(from_y, to_y + 1):
                        blocked_coord = (
                            curr_x,
                            i_y,
                        )
                        bisect.insort(blocked, blocked_coord)
                else:
                    raise Exception("unexpected")
    return blocked


def index(lst, x):
    i = bisect.bisect_left(lst, x)
    if i != len(lst) and lst[i] == x:
        return i
    return None


def is_free(coord, blocked, sands):
    if index(blocked, coord) is None and index(sands, coord) is None:
        return True
    else:
        return False


def is_block_below(x, y, blocked):
    below = next((coord for coord in blocked if coord[0] == x and coord[1] > y), None)
    return below is not None


def add_sand(blocked: list[tuple[int, int]], sands: list[tuple[int, int]]):
    curr_x, curr_y = (500, 0)
    overflow = False
    at_rest = False
    while not at_rest:
        # Do we get overflow?
        if not is_block_below(curr_x, curr_y, blocked):
            overflow = True
            break

        # Can move down?
        if is_free((curr_x, curr_y + 1), blocked, sands):
            curr_y += 1
        else:
            if is_free((curr_x - 1, curr_y + 1), blocked, sands):
                curr_x -= 1
                curr_y += 1
            elif is_free((curr_x + 1, curr_y + 1), blocked, sands):
                curr_x += 1
                curr_y += 1
            else:
                bisect.insort(sands, (curr_x, curr_y))
                # print_current(blocked, sands)
                at_rest = True

    return not overflow


filename = "14/input"
blocked = parse_input(filename)

# print("Blocked coords:")
print(blocked)

sands = []
while add_sand(blocked, sands):
    pass

sands_at_rest = len(sands)
print("Part1:", sands_at_rest)  # 808
