from collections import defaultdict
import heapq
import re
import sys
import os


# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid

EAST = Grid.Pos(0, 1)
WEST = Grid.Pos(0, -1)
NORTH = Grid.Pos(-1, 0)
SOUTH = Grid.Pos(1, 0)


def parse(filename: str) -> list[Grid.Pos]:
    rows = -1
    cols = -1
    positions = []
    with open(filename) as f:
        for line in f:
            tmp = list(map(int, re.findall(r"\d+", line)))
            row = tmp[1]
            col = tmp[0]
            rows = max(rows, row + 1)
            cols = max(cols, col + 1)
            positions.append(Grid.Pos(row, col))
    return positions, rows, cols


def make_grid(positions: list[Grid.Pos], rows, cols) -> Grid:
    grid = Grid(rows, cols, ".")
    for pos in positions:
        grid.set_by_pos(pos, "#")

    return grid


def dijkstra(grid: Grid, start: Grid.Pos) -> dict[Grid.Pos, int]:
    # priority queue: (distance, pos)
    pq = [(0, start)]

    distances = defaultdict(lambda: sys.maxsize)
    distances[start] = 0

    visited = set()

    while pq:
        curr_dist, curr_pos = heapq.heappop(pq)

        if curr_pos in visited:
            continue

        visited.add(curr_pos)

        for step in [EAST, WEST, NORTH, SOUTH]:
            next_pos = curr_pos + step

            if not grid.is_pos_within_bounds(next_pos):
                continue

            val = grid.get_by_pos(next_pos)
            if val == "#":
                continue

            next_dist = curr_dist + 1

            # If a shorter path to the neighbor is found
            if next_dist < distances[next_pos]:
                distances[next_pos] = next_dist
                heapq.heappush(pq, (next_dist, next_pos))

    return distances


def part1(filename: str):
    positions, rows, cols = parse(filename)

    if "example" in filename:
        positions = positions[:12]
    else:
        positions = positions[:1024]

    grid = make_grid(positions, rows, cols)
    start = Grid.Pos(0, 0)
    end = Grid.Pos(grid.rows - 1, grid.cols - 1)

    distances = dijkstra(grid, start)
    shortest_dist = distances[end]

    print("Part 1:", shortest_dist)


def is_path_blocked(positions: list[Grid.Pos], rows, cols) -> bool:
    grid = make_grid(positions, rows, cols)
    start = Grid.Pos(0, 0)
    end = Grid.Pos(grid.rows - 1, grid.cols - 1)

    distances = dijkstra(grid, start)
    shortest_dist = distances[end]

    return shortest_dist == sys.maxsize


def part2(filename: str):
    positions, rows, cols = parse(filename)

    left = 1
    right = len(positions) - 1
    while left < right:
        mid = (left + right) // 2
        if is_path_blocked(positions[:mid], rows, cols):
            right = mid
        else:
            left = mid + 1

    assert is_path_blocked(positions[:mid], rows, cols)
    assert not is_path_blocked(positions[: mid - 1], rows, cols)

    pos = positions[left - 1]
    msg = f"{pos.col},{pos.row}"
    print("Part 2:", msg)


# filename = "day18/example"
filename = "day18/input"


part1(filename)
part2(filename)
