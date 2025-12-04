from collections import defaultdict


Grid = defaultdict
grid_row_cnt = 0
grid_col_cnt = 0


def parse(filename) -> Grid:
    global grid_row_cnt, grid_col_cnt

    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    grid_row_cnt = len(lines)
    grid_col_cnt = len(lines[0])

    grid = Grid(lambda: ".")

    for r in range(grid_row_cnt):
        for c in range(grid_col_cnt):
            grid[(r, c)] = lines[r][c]

    return grid


def find_removable(grid: Grid) -> list[tuple[int, int]]:
    global grid_row_cnt, grid_col_cnt

    removable = []
    for r in range(grid_row_cnt):
        for c in range(grid_col_cnt):
            curr_val = grid[(r, c)]
            if curr_val == "@":
                # get neighbors in all 8 directions
                neighbor_vals = [
                    grid[(r - 1, c - 1)],
                    grid[(r - 1, c)],
                    grid[(r - 1, c + 1)],
                    grid[(r, c - 1)],
                    grid[(r, c + 1)],
                    grid[(r + 1, c - 1)],
                    grid[(r + 1, c)],
                    grid[(r + 1, c + 1)],
                ]

                cnt = neighbor_vals.count("@")
                if cnt < 4:
                    removable.append((r, c))

    return removable


def remove(grid: Grid, positions: list[tuple[int, int]]):
    for pos in positions:
        grid[pos] = "."


def part1(grid: Grid):
    removable = find_removable(grid)

    print("Part 1:", len(removable))


def part2(grid: Grid):
    total_removed = 0

    while True:
        removable = find_removable(grid)
        if len(removable) == 0:
            break

        remove(grid, removable)
        total_removed += len(removable)

    print("Part 2:", total_removed)


filename = "day04/example"
filename = "day04/input"

grid = parse(filename)

part1(grid)
part2(grid)
