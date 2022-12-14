import bisect

"""
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def print_current(blocked):
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

    for x, y in blocked:
        norm_y = y - min_y
        norm_x = x - min_x + 1
        lines[norm_y][norm_x] = "#"

    for i, line in enumerate(lines):
        print(i, " ", "".join(line))


def parse_input(filename):
    blocked = []

    with open(filename) as f:
        prev_x = prev_y = None
        for line in f:
            print("Parsing line: ", line)
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


filename = "14/example"
blocked = parse_input(filename)

print("Blocked coords:")
print(blocked)

print_current(blocked)

print("Done")
