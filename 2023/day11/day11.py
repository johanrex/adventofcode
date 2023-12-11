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


def get_empty_row_cols(grid):
    # rows
    empty_rows = []
    for r, line in enumerate(grid):
        if all(c == "." for c in line):
            empty_rows.append(r)

    grid = flip_grid(grid)

    # cols
    empty_cols = []
    for c_nr, line in enumerate(grid):
        if all(c == "." for c in line):
            empty_cols.append(c_nr)

    return empty_rows, empty_cols


def get_nodes(grid):
    nodes = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "#":
                nodes.append((row, col))
    return nodes


def part1(grid):
    grid = expand(grid)
    nodes = get_nodes(grid)

    # nodes pair-wise
    pairs = list(combinations(nodes, 2))

    s = 0

    for pair in pairs:
        start, end = pair
        startx, starty = start
        endx, endy = end
        d = abs(startx - endx) + abs(starty - endy)

        s += d

    print("Part 1:", s)


def part2(grid):
    empty_rows, empty_cols = get_empty_row_cols(grid)

    empty_rows.sort(reverse=True)
    empty_cols.sort(reverse=True)

    nodes = get_nodes(grid)

    expansion_nr = 1_000_000
    expansion_nr = expansion_nr - 1

    nodes.sort()
    for empty_row in empty_rows:
        for i, node in enumerate(nodes):
            if node[0] > empty_row:
                new_node = (node[0] + expansion_nr, node[1])
                nodes[i] = new_node

    nodes.sort(key=lambda node: node[1])
    for empty_col in empty_cols:
        for i, node in enumerate(nodes):
            if node[1] > empty_col:
                new_node = (node[0], node[1] + expansion_nr)
                nodes[i] = new_node

    # nodes pair-wise
    pairs = list(combinations(nodes, 2))

    s = 0

    for pair in pairs:
        start, end = pair
        startx, starty = start
        endx, endy = end
        d = abs(startx - endx) + abs(starty - endy)

        s += d

    print("Part 2:", s)


# filename = "day11/example"
filename = "day11/input"

grid = parse(filename)
part1(grid)
part2(grid)
