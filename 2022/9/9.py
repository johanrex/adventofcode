from dataclasses import dataclass


@dataclass
class Move:
    direction: str
    steps: int


@dataclass
class Coordinate:
    x: int
    y: int


def step(from_h: Coordinate, from_t: Coordinate, move: Move) -> tuple[Coordinate, Coordinate]:
    global unique_tail_pos

    to_h = Coordinate(from_h.x, from_h.y)
    to_t = Coordinate(from_t.x, from_t.y)

    match move.direction:
        case "R":
            to_h.x += move.steps
        case "L":
            to_h.x -= move.steps
        case "U":
            to_h.y += move.steps
        case "D":
            to_h.y -= move.steps

    delta_x = to_h.x - from_t.x
    delta_y = to_h.y - from_t.y

    diag_skip = int(abs(delta_x) > 0 and abs(delta_y) > 0)

    if (0 <= abs(delta_x) <= 1) and (0 <= abs(delta_y) <= 1):
        # Nothing to do.
        pass
    elif abs(delta_x) >= 2 or abs(delta_y) >= 2:
        match move.direction:
            case "R":
                to_t.x = to_h.x - 1
                to_t.y = to_h.y
                start = min(from_t.x, to_t.x) + diag_skip
                stop = max(from_t.x, to_t.x) + 1
                unique_tail_pos = unique_tail_pos | {(x, to_t.y) for x in range(start, stop)}
            case "L":
                to_t.x = to_h.x + 1
                to_t.y = to_h.y
                start = min(from_t.x, to_t.x)
                stop = max(from_t.x, to_t.x)
                unique_tail_pos = unique_tail_pos | {(x, to_t.y) for x in range(start, stop)}
            case "U":
                to_t.y = to_h.y - 1
                to_t.x = to_h.x
                start = min(from_t.y, to_t.y) + diag_skip
                stop = max(from_t.y, to_t.y) + 1
                unique_tail_pos = unique_tail_pos | {(to_t.x, y) for y in range(start, stop)}
            case "D":
                to_t.y = to_h.y + 1
                to_t.x = to_h.x
                # start = min(from_t.y, to_t.y) + diag_skip
                # stop = max(from_t.y, to_t.y) + 1
                start = min(from_t.y, to_t.y)
                stop = max(from_t.y, to_t.y)

                unique_tail_pos = unique_tail_pos | {(to_t.x, y) for y in range(start, stop)}
    return to_h, to_t


def get_grid():
    gridsize = 10
    grid = []
    for _ in range(gridsize):
        grid.append(["."] * gridsize)
    return grid


def print_unique_tail_pos():
    global unique_tail_pos
    grid = get_grid()

    for tpl in unique_tail_pos:
        x, y = tpl
        grid[y][x] = "#"

    for line in reversed(grid):
        print("".join(line))
    print("---")


def print_state(h: Coordinate, t: Coordinate):
    grid = get_grid()
    grid[t.y][t.x] = "T"
    grid[h.y][h.x] = "H"

    for line in reversed(grid):
        print("".join(line))
    print("---")


# filename = "9/example"
filename = "9/input"
moves = []
with open(filename) as f:
    for line in f:
        a, b = line.strip().split()
        moves.append(Move(a, int(b)))

h = Coordinate(0, 0)
t = Coordinate(0, 0)


unique_tail_pos = set()
unique_tail_pos.add((0, 0))
for move in moves:
    print(move)
    h, t = step(h, t, move)
    # print_state(h, t)
    # print_unique_tail_pos()
    pass

# 6173 too low.
# 6349 too high
print("Part1:", len(unique_tail_pos))
