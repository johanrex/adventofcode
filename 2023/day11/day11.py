from itertools import combinations


def parse(filename):
    grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            grid.append(line)
    return grid


def print_grid(grid):
    for row in grid:
        print(row)


def flip_grid(grid):
    new_grid = []
    for c in range(len(grid[0])):
        new_row = ""
        for r in range(len(grid)):
            new_row += grid[r][c]
        new_grid.append(new_row)
    return new_grid


def expand(grid):
    # rows
    new_rows = []
    for line in grid:
        if all(c == "." for c in line):
            new_rows.append(line)

        new_rows.append(line)
    grid = new_rows

    grid = flip_grid(grid)

    # cols
    new_cols = []
    for line in grid:
        if all(c == "." for c in line):
            new_cols.append(line)

        new_cols.append(line)
    grid = new_cols

    grid = flip_grid(grid)
    return grid


def get_nodes(grid):
    nodes = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "#":
                nodes.append((row, col))
    return nodes


from collections import deque


def shortest_path(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, 0)])
    visited = set([start])

    while queue:
        (x, y), step = queue.popleft()

        if (x, y) == end:
            return step

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < rows
                and 0 <= ny < cols
                # and grid[nx][ny] == "."
                and (nx, ny) not in visited
            ):
                queue.append(((nx, ny), step + 1))
                visited.add((nx, ny))

    return -1  # No path found


def part1(grid):
    grid = expand(grid)
    # print("expanded:")
    # print_grid(grid)

    nodes = get_nodes(grid)
    # print("nodes:", nodes)

    # nodes pair-wise
    pairs = list(combinations(nodes, 2))

    s = 0

    for pair in pairs:
        start, end = pair
        # print(start, end)
        d = shortest_path(grid, start, end)
        s += d

    print("Part 1:", s)


def part2(grid):
    pass
    # print("Part 2:", grid)


# filename = "day11/example"
filename = "day11/input"

grid = parse(filename)
part1(grid)
part2(grid)
