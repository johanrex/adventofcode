import math
from collections import deque


def parse(filename):
    grid = []
    with open(filename) as f:
        for line in f:
            chars = [c for c in line.strip()]
            grid.append(chars)
    return grid


def find_s(grid) -> tuple[int, int]:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                return row, col
    return (-1, -1)


def get_neighbors(grid, vertex) -> list[tuple[int, int]]:
    row, col = vertex
    neighbors = []

    if grid[row][col] == "S":
        west = grid[row][col - 1] if col > 0 else None
        if west is not None and west in "SFL-":
            neighbors.append((row, col - 1))

        east = grid[row][col + 1] if col < len(grid[row]) - 1 else None
        if east is not None and east in "SJ7-":
            neighbors.append((row, col + 1))

        north = grid[row - 1][col] if row > 0 else None
        if north is not None and north in "SF7|":
            neighbors.append((row - 1, col))

        south = grid[row + 1][col] if row < len(grid) - 1 else None
        if south is not None and south in "SJL|":
            neighbors.append((row + 1, col))

    elif grid[row][col] == "|":
        north = grid[row - 1][col] if row > 0 else None
        if north is not None and north in "SF7|":
            neighbors.append((row - 1, col))

        south = grid[row + 1][col] if row < len(grid) - 1 else None
        if south is not None and south in "SJL|":
            neighbors.append((row + 1, col))

    elif grid[row][col] == "-":
        west = grid[row][col - 1] if col > 0 else None
        if west is not None and west in "SFL-":
            neighbors.append((row, col - 1))

        east = grid[row][col + 1] if col < len(grid[row]) - 1 else None
        if east is not None and east in "SJ7-":
            neighbors.append((row, col + 1))

    elif grid[row][col] == "L":
        north = grid[row - 1][col] if row > 0 else None
        if north is not None and north in "SF7|":
            neighbors.append((row - 1, col))

        east = grid[row][col + 1] if col < len(grid[row]) - 1 else None
        if east is not None and east in "SJ7-":
            neighbors.append((row, col + 1))

    elif grid[row][col] == "J":
        north = grid[row - 1][col] if row > 0 else None
        if north is not None and north in "SF7|":
            neighbors.append((row - 1, col))

        west = grid[row][col - 1] if col > 0 else None
        if west is not None and west in "SFL-":
            neighbors.append((row, col - 1))

    elif grid[row][col] == "7":
        south = grid[row + 1][col] if row < len(grid) - 1 else None
        if south is not None and south in "SJL|":
            neighbors.append((row + 1, col))

        west = grid[row][col - 1] if col > 0 else None
        if west is not None and west in "SFL-":
            neighbors.append((row, col - 1))

    elif grid[row][col] == "F":
        south = grid[row + 1][col] if row < len(grid) - 1 else None
        if south is not None and south in "SJL|":
            neighbors.append((row + 1, col))

        east = grid[row][col + 1] if col < len(grid[row]) - 1 else None
        if east is not None and east in "SJ7-":
            neighbors.append((row, col + 1))

    return neighbors


def print_path(grid, path):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if (row, col) in path:
                print(grid[row][col], end="")
            else:
                print(".", end="")
        print()


def print_grid(grid):
    for row in range(len(grid)):
        print("".join(grid[row]))


def find_cycle(start_vertex, grid):
    visited = set()
    stack = [(start_vertex, None)]
    parent = {start_vertex: None}

    while stack:
        vertex, parent_vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            neighbors = get_neighbors(grid, vertex)

            for neighbor in neighbors:
                if neighbor not in visited:
                    parent[neighbor] = vertex
                    stack.append((neighbor, vertex))
                elif neighbor != parent_vertex:
                    # Cycle detected. Construct the cycle path.
                    path = []
                    while vertex != neighbor:
                        path.append(vertex)
                        vertex = parent[vertex]
                    path.append(neighbor)
                    path.reverse()
                    return path

    raise ValueError("No cycle found")


def flood_fill(grid, row, col, new_color):
    # Store the original color of the starting point
    old_color = grid[row][col]

    # If the starting point is already the new color, return
    if old_color == new_color:
        return

    # Queue for BFS
    queue = deque([(row, col)])

    while queue:
        r, c = queue.popleft()

        if (
            r < 0
            or r >= len(grid)
            or c < 0
            or c >= len(grid[0])
            or grid[r][c] != old_color
        ):
            continue

        grid[r][c] = new_color

        queue.append((r + 1, c))
        queue.append((r - 1, c))
        queue.append((r, c + 1))
        queue.append((r, c - 1))


def part1(cycle):
    row, col = find_s(grid)
    # row, col = 1, 1

    # print(path)

    cycle = find_cycle((row, col), grid)
    print_path(grid, cycle)

    farthest_cell = math.ceil(len(cycle) / 2)

    print("Part 1:", farthest_cell)


def replace_not_in_cycle(grid, cycle, val):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if (row, col) not in cycle:
                grid[row][col] = val


def add_border(grid, border_val) -> list[list[str]]:
    bordered_grid: list[list[str]] = []

    for row in grid:
        bordered_grid.append([border_val] + row + [border_val])

    bordered_grid.insert(0, [border_val] * len(bordered_grid[0]))
    bordered_grid.append([border_val] * len(bordered_grid[0]))

    return bordered_grid


def remove_border(bordered_grid) -> list[list[str]]:
    stripped_grid = []
    for row in bordered_grid:
        stripped_grid.append(row[1:-1])

    return stripped_grid


def is_inside_polygon(vertex, grid, cycle) -> bool:
    row, col = vertex
    chars = "|LJ7F"
    c = cycle
    vertices_before = [(r, c) for r, c in c if r == row and c < col]
    walls_before = [(r, c) for r, c in vertices_before if grid[r][c] in chars]
    n = len(walls_before)

    return n % 2 == 1


def replace_s(grid):
    vertex_s = find_s(grid)
    vn = get_neighbors(grid, vertex_s)

    # true for this specific input
    assert len(vn) == 2

    # let's hardcode these, could be solved better
    from_to_lookup = {
        "F|": "7",
        "7|": "|",
    }

    neighbor_vals = [grid[vn[0][0]][vn[0][1]], grid[vn[1][0]][vn[1][1]]]
    key = "".join(neighbor_vals)
    s = from_to_lookup[key]

    grid[vertex_s[0]][vertex_s[1]] = s

    return grid


def part2(grid):
    row, col = find_s(grid)
    # row, col = 1, 1

    # print(path)
    # print_path(grid, path)

    cycle = find_cycle((row, col), grid)
    replace_s(grid)

    replace_not_in_cycle(grid, cycle, ".")

    # print_grid(grid)

    flood_fill(grid, 0, 0, "O")
    print_grid(grid)

    nr_inside_polygon = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # for col in range(len(grid[row]) - 1, -1, -1):
            if grid[row][col] == ".":
                if is_inside_polygon((row, col), grid, cycle):
                    grid[row][col] = "I"
                    nr_inside_polygon += 1
                else:
                    grid[row][col] = "O"

    print_grid(grid)

    print("Part 2:", nr_inside_polygon)

    # row, col = 0, 0
    # bordered_grid = add_border(grid, ".")
    # flood_fill(bordered_grid, 1, 1, "O")
    # grid = remove_border(bordered_grid)


# filename = "day10/example"
filename = "day10/input"

grid = parse(filename)
# part1(grid)
part2(grid)
