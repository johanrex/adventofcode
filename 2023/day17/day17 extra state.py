from dataclasses import dataclass
import math
import re
import heapq
import copy
from collections import deque
import sys
import json


Grid = list[list[int]]


@dataclass
class State:
    row: int
    col: int
    direction: tuple[int, int]
    steps: int

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        return State(**json.loads(json_str))

    def __hash__(self) -> int:
        return hash(self.to_json())

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, State):
            return False
        return self.to_json() == o.to_json()


def parse(filename) -> Grid:
    grid: Grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            grid.append([int(c) for c in line])

    return grid


def dijkstra(grid, start_coord):
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    ]
    n_rows, n_cols = len(grid), len(grid[0])
    cost_dict = {}
    prev_dict = {}

    state = State(row=start_coord[0], col=start_coord[1], direction=(0, 0), steps=1)

    cost_dict[state] = 0
    queue = [(0, state.to_json())]

    while queue:
        curr_cost, curr_state_json = heapq.heappop(queue)
        curr_state = State.from_json(curr_state_json)
        curr_row = curr_state.row
        curr_col = curr_state.col
        curr_direction = curr_state.direction
        curr_steps = curr_state.steps

        # print(f"At {curr_row}, {curr_col}.")

        if curr_cost != cost_dict[curr_state]:
            raise Exception("Does this ever happen?")
            continue  # TODO does this ever happen?

        for next_direction in directions:
            d_row, d_col = next_direction
            next_row, next_col = curr_row + d_row, curr_col + d_col
            if 0 <= next_row < n_rows and 0 <= next_col < n_cols:  # Check boundaries
                # print(
                #     f"At {curr_row} {curr_col}. Considering next:", next_row, next_col
                # )

                if curr_direction == next_direction:
                    if curr_steps >= 3:
                        continue
                    else:
                        next_steps = curr_steps + 1
                else:
                    next_steps = 1

                next_state = State(
                    row=next_row,
                    col=next_col,
                    direction=next_direction,
                    steps=next_steps,
                )

                if next_state in cost_dict:
                    existing_cost = cost_dict[next_state]
                else:
                    existing_cost = sys.maxsize

                alt_c = curr_cost + grid[next_row][next_col]

                if alt_c < existing_cost:
                    cost_dict[next_state] = alt_c
                    prev_dict[next_state] = curr_state
                    heapq.heappush(queue, (alt_c, next_state.to_json()))

    return cost_dict, prev_dict


def reconstruct_dijkstra_path(prev, target):
    x, y = target
    path = []

    while x is not None and y is not None:
        path.append((x, y))
        tmp = prev[x][y]
        if tmp is None:
            break
        x, y = tmp

    path.reverse()
    return path


def print_dijkstra_path(grid, prev_grid, start, goal_state):
    g = copy.deepcopy(grid)

    current = goal_state
    while (current.row, current.col) != start:
        prev = prev_grid[current]

        curr_row = current.row
        curr_col = current.col
        prev_row = prev.row
        prev_col = prev.col

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

    cost_dict, prev_dict = dijkstra(grid, start)

    candidates = [
        state
        for state in cost_dict.keys()
        if state.row == goal[0] and state.col == goal[1]
    ]

    min_cost = sys.maxsize
    goal_state = None
    for state in candidates:
        if cost_dict[state] < min_cost:
            min_cost = cost_dict[state]
            goal_state = state

    print_dijkstra_path(grid, prev_dict, start, goal_state)

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
