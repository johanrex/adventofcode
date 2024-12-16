import sys
import os
import time
import heapq

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid

EAST = Grid.Pos(0, 1)
WEST = Grid.Pos(0, -1)
NORTH = Grid.Pos(-1, 0)
SOUTH = Grid.Pos(1, 0)


def parse(filename: str) -> tuple[Grid, Grid.Pos, list[str]]:
    with open(filename) as f:
        content = f.read().strip()

    lines = content.split("\n")
    rows = len(lines)
    cols = len(lines[0])
    grid = Grid(rows, cols)

    start = None
    end = None

    for row, line in enumerate(lines):
        line = line.strip()

        for col, val in enumerate(line):
            grid.set(row, col, val)
            if val == "S":
                assert start is None
                start = Grid.Pos(row, col)
            elif val == "E":
                assert end is None
                end = Grid.Pos(row, col)

            grid.set(row, col, val)

    return grid, start, end


def print_path(grid: Grid, path: list[Grid.Pos]):
    grid_copy = grid.copy()

    # set directions
    next_dir = EAST
    for i, pos in enumerate(path):
        if i == 0 or i == len(path) - 1:
            continue

        next_dir = path[i + 1] - path[i]

        if next_dir == EAST:
            grid_copy.set_by_pos(pos, ">")
        elif next_dir == WEST:
            grid_copy.set_by_pos(pos, "<")
        elif next_dir == NORTH:
            grid_copy.set_by_pos(pos, "^")
        elif next_dir == SOUTH:
            grid_copy.set_by_pos(pos, "v")

    # draw glorious grid with path
    for row in range(grid_copy.rows):
        line = ""
        for col in range(grid_copy.cols):
            pos = Grid.Pos(row, col)
            line += grid_copy.get_by_pos(pos)
        print(line)


def dijkstra(grid: Grid, start: Grid.Pos, facing_dir: Grid.Pos) -> dict[Grid.Pos, int]:
    # (distance, pos, facing direction)
    pq = [(0, start, facing_dir)]

    # init distances
    distances = dict()
    for row in range(grid.rows):
        for col in range(grid.cols):
            pos = Grid.Pos(row, col)
            val = grid.get_by_pos(pos)
            if val != "#":
                distances[pos] = float("inf")

    distances[start] = 0
    visited = set()

    while pq:
        curr_dist, curr_pos, facing = heapq.heappop(pq)

        if curr_pos in visited:
            continue
        visited.add(curr_pos)

        for next_facing in [EAST, WEST, NORTH, SOUTH]:
            next_pos = curr_pos + next_facing

            val = grid.get_by_pos(next_pos)
            if val == "#":
                continue

            next_dist = curr_dist + 1
            if facing != next_facing:
                next_dist += 1000

            # If a shorter path to the neighbor is found
            if next_dist < distances[next_pos]:
                distances[next_pos] = next_dist
                heapq.heappush(pq, (next_dist, next_pos, next_facing))

    return distances


def solve(grid: Grid, start: Grid.Pos, end: Grid.Pos):
    distances = dijkstra(grid, start, EAST)

    min_dist = distances[end]
    print("Part 1:", min_dist)

    d1 = dijkstra(grid, end, EAST)
    d2 = dijkstra(grid, end, WEST)
    d3 = dijkstra(grid, end, NORTH)
    d4 = dijkstra(grid, end, SOUTH)

    tiles = set()

    for row in range(grid.rows):
        for col in range(grid.cols):
            pos = Grid.Pos(row, col)
            if grid.get_by_pos(pos) != "#":
                s_to_e_dist = distances[pos]
                e_to_s_dist1 = d1[pos]
                e_to_s_dist2 = d2[pos]
                e_to_s_dist3 = d3[pos]
                e_to_s_dist4 = d4[pos]

                if (
                    (s_to_e_dist + e_to_s_dist1 == min_dist)
                    or (s_to_e_dist + e_to_s_dist2 == min_dist)
                    or (s_to_e_dist + e_to_s_dist3 == min_dist)
                    or (s_to_e_dist + e_to_s_dist4 == min_dist)
                ):
                    tiles.add(pos)

    print("Part 2:", len(tiles))


start_time = time.perf_counter()

# filename = "day16/example"
filename = "day16/input"

grid, start, end = parse(filename)
solve(grid, start, end)

end_time = time.perf_counter()
print(f"Total time: {end_time - start_time} seconds")
