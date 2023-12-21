from dataclasses import dataclass
import math
import re
import heapq
import copy
from collections import deque
import sys

Grid = list[list[int]]


# def heuristic(a, b, cost):
#     return abs(a[0] - b[0]) + abs(a[1] - b[1]) + cost


# def a_star_search(grid, start, goal):
#     neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#     queue = []
#     heapq.heappush(queue, (0, start, None, 0))  # Add direction and steps to queue
#     path = {}
#     cost = {start: 0}

#     while queue:
#         _, current, direction, steps = heapq.heappop(queue)

#         if current == goal:
#             break

#         for dx, dy in neighbors:
#             nxt = (current[0] + dx, current[1] + dy)

#             if 0 <= nxt[0] < len(grid) and 0 <= nxt[1] < len(grid[0]):
#                 next_cost = cost[current] + grid[nxt[0]][nxt[1]]
#                 if nxt not in cost or next_cost < cost[nxt]:
#                     if (
#                         (dx, dy) == direction and steps < 3
#                     ):  # Same direction and less than 3 steps
#                         cost[nxt] = next_cost
#                         priority = next_cost + heuristic(
#                             goal, nxt, grid[nxt[0]][nxt[1]]
#                         )
#                         heapq.heappush(queue, (priority, nxt, (dx, dy), steps + 1))
#                         path[nxt] = current
#                     elif (dx, dy) != direction:  # Different direction
#                         cost[nxt] = next_cost
#                         priority = next_cost + heuristic(
#                             goal, nxt, grid[nxt[0]][nxt[1]]
#                         )
#                         heapq.heappush(queue, (priority, nxt, (dx, dy), 1))
#                         path[nxt] = current

#     return path, cost


def parse(filename) -> Grid:
    grid: Grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            grid.append([int(c) for c in line])

    return grid


# def print_path(grid, path, start, goal):
#     g = copy.deepcopy(grid)

#     current = goal
#     while current != start:
#         prev = path[current]

#         curr_row, curr_col = current
#         prev_row, prev_col = prev

#         d_r = curr_row - prev_row
#         d_c = curr_col - prev_col

#         assert abs(d_r) == 1 or abs(d_c) == 1

#         if d_r == 1:
#             g[curr_row][curr_col] = "v"
#         elif d_r == -1:
#             g[curr_row][curr_col] = "^"
#         elif d_c == 1:
#             g[curr_row][curr_col] = ">"
#         elif d_c == -1:
#             g[curr_row][curr_col] = "<"

#         current = prev

#     for row in g:
#         print("".join([str(c) for c in row]))


def dijkstra(grid, start):
    def can_move(row_from: int, col_from: int, row_to: int, col_to: int) -> bool:
        limit = 3

        prev_direction = (row_to - row_from, col_to - col_from)
        direction_cnt = 1

        cur = (row_from, col_from)

        if cur != start:
            for _ in range(limit):
                prev = prev_grid[cur[0]][cur[1]]

                # prev can be None for the first cell
                if prev is None:
                    break

                direction = (cur[0] - prev[0], cur[1] - prev[1])

                if direction != prev_direction:
                    direction_cnt = 0
                    break
                else:
                    direction_cnt += 1
                    if direction_cnt >= 3:
                        break

                cur = prev
                prev_direction = direction

        retval = direction_cnt != limit

        print("Can move from", row_from, col_from, "to", row_to, col_to, "?", retval)
        return retval

    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    ]
    n_rows, n_cols = len(grid), len(grid[0])
    cost_grid = [[sys.maxsize] * n_cols for _ in range(n_rows)]
    prev_grid = [[None] * n_cols for _ in range(n_rows)]
    cost_grid[start[0]][start[1]] = 0
    queue = [(0, start)]

    while queue:
        c, (row, col) = heapq.heappop(queue)

        print(f"At {row}, {col}.")

        if c != cost_grid[row][col]:
            continue

        for d_row, d_col in directions:
            next_row, next_col = row + d_row, col + d_col
            if 0 <= next_row < n_rows and 0 <= next_col < n_cols:  # Check boundaries
                print(f"At {row} {col}. Considering next:", next_row, next_col)
                if not can_move(row, col, next_row, next_col):
                    continue

                alt_c = c + grid[next_row][next_col]
                if alt_c < cost_grid[next_row][next_col]:
                    cost_grid[next_row][next_col] = alt_c
                    prev_grid[next_row][next_col] = (
                        row,
                        col,
                    )  # Store the previous cell
                    heapq.heappush(queue, (alt_c, (next_row, next_col)))

    return cost_grid, prev_grid


def reconstruct_dijkstra_path(prev, target):
    x, y = target
    path = []

    while x is not None and y is not None:
        path.append((x, y))
        tmp = prev[x][y]
        if tmp is None:
            break
        x, y = tmp

    path.reverse()  # Reverse the path to go from start to target
    return path


def print_dijkstra_path(grid, prev_grid, start, goal):
    g = copy.deepcopy(grid)

    current = goal
    while current != start:
        curr_row, curr_col = current
        prev = prev_grid[curr_row][curr_col]

        prev_row, prev_col = prev

        d_r = curr_row - prev_row
        d_c = curr_col - prev_col

        assert abs(d_r) == 1 or abs(d_c) == 1

        if d_r == 1:
            g[curr_row][curr_col] = "v"
        elif d_r == -1:
            g[curr_row][curr_col] = "^"
        elif d_c == 1:
            g[curr_row][curr_col] = ">"
        elif d_c == -1:
            g[curr_row][curr_col] = "<"

        current = prev

    for row in g:
        print("".join([str(c) for c in row]))


def part1(grid: Grid):
    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    # path, cost = a_star_search(grid, start, goal)
    # print_path(grid, path, start, goal)

    cost_grid, prev_grid = dijkstra(grid, start)
    # path = reconstruct_dijkstra_path(prev_grid, goal)
    print_dijkstra_path(grid, prev_grid, start, goal)

    print(cost_grid[goal[0]][goal[1]])

    pass

    # 656 too high
    # print("Part 1:", cost[goal])


def part2(grid: Grid):
    print("Part 2:", -1)


filename = "day17/example"
# filename = "day17/input"

grid = parse(filename)
part1(grid)
part2(grid)
