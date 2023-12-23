from dataclasses import dataclass
import math
import re
import heapq
import copy
from collections import deque
import sys
import json


Grid = list[list[int]]


def parse(filename) -> Grid:
    grid: Grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            grid.append([int(c) for c in line])

    return grid


def search(grid):
    n_rows, n_cols = len(grid), len(grid[0])

    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    ]

    end_coord = (n_rows - 1, n_cols - 1)

    # heat_loss, cur_row, cur_col, d_row, d_col, steps_in_direction
    queue = [(0, 0, 0, 0, 0, 0)]
    seen = set()

    while queue:
        heat_loss, cur_row, cur_col, d_row, d_col, steps_in_direction = heapq.heappop(
            queue
        )

        if end_coord == (cur_row, cur_col):
            break

        if (cur_row, cur_col, d_row, d_col, steps_in_direction) in seen:
            continue

        seen.add((cur_row, cur_col, d_row, d_col, steps_in_direction))

        # take the step
        if steps_in_direction < 3 and (d_row, d_col) != (0, 0):
            nr = cur_row + d_row
            nc = cur_col + d_col
            if 0 <= nr < n_rows and 0 <= nc < n_cols:
                heapq.heappush(
                    queue,
                    (
                        heat_loss + grid[nr][nc],
                        nr,
                        nc,
                        d_row,
                        d_col,
                        steps_in_direction + 1,
                    ),
                )

        for next_d_row, next_d_col in directions:
            if (next_d_row, next_d_col) != (d_row, d_col) and (
                next_d_row,
                next_d_col,
            ) != (-d_row, -d_col):
                nr = cur_row + next_d_row
                nc = cur_col + next_d_col
                if 0 <= nr < n_rows and 0 <= nc < n_cols:
                    heapq.heappush(
                        queue,
                        (
                            heat_loss + grid[nr][nc],
                            nr,
                            nc,
                            next_d_row,
                            next_d_col,
                            1,
                        ),
                    )

    return heat_loss


def part1(grid: Grid):
    heat_loss = search(grid)
    print("Part 1:", heat_loss)


def part2(grid: Grid):
    print("Part 2:", -1)


filename = "day17/example"
# filename = "day17/input"

grid = parse(filename)
part1(grid)
# part2(grid)
