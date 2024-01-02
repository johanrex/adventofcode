import heapq
import copy

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
    queue = [(0, 0, 0, -1, -1, 0)]
    seen = set()

    while queue:
        heat_loss, cur_row, cur_col, d_row, d_col, steps_in_direction = heapq.heappop(
            queue
        )

        # print(
        #     f"{heat_loss=}, {cur_row=}, {cur_col=}, {d_row=}, {d_col=}, {steps_in_direction=}"
        # )

        if (cur_row, cur_col, d_row, d_col, steps_in_direction) in seen:
            continue

        seen.add((cur_row, cur_col, d_row, d_col, steps_in_direction))

        # Have we reached the goal?
        if end_coord == (cur_row, cur_col) and 4 <= steps_in_direction <= 10:
            break

        if (
            steps_in_direction <= 3
            # and steps_in_direction <= 10
            and (d_row, d_col) != (-1, -1)
        ):
            next_row = cur_row + d_row
            next_col = cur_col + d_col
            if 0 <= next_row < n_rows and 0 <= next_col < n_cols:
                heapq.heappush(
                    queue,
                    (
                        heat_loss + grid[next_row][next_col],
                        next_row,
                        next_col,
                        d_row,
                        d_col,
                        steps_in_direction + 1,
                    ),
                )
        else:
            for next_d_row, next_d_col in directions:
                # Don't go back to the same place we came from
                if (next_d_row, next_d_col) == (-d_row, -d_col):
                    continue

                next_row = cur_row + next_d_row
                next_col = cur_col + next_d_col
                if 0 <= next_row < n_rows and 0 <= next_col < n_cols:
                    if d_row == next_d_row and d_col == next_d_col:
                        next_steps_in_direction = steps_in_direction + 1
                    else:
                        next_steps_in_direction = 1

                    if next_steps_in_direction <= 10:
                        heapq.heappush(
                            queue,
                            (
                                heat_loss + grid[next_row][next_col],
                                next_row,
                                next_col,
                                next_d_row,
                                next_d_col,
                                next_steps_in_direction,
                            ),
                        )

    # print(heat_loss)
    # print_path(grid, seen, end_coord)

    return heat_loss


def print_path(
    grid: Grid,
    seen: set[tuple[int, int, int, int, int]],
    end_coord: tuple[int, int],
):
    g = [[str(item) for item in row] for row in grid]

    curr_coord = end_coord
    while curr_coord is not None:
        curr_row, curr_col = curr_coord
        candidates = {tpl for tpl in seen if tpl[0] == curr_row and tpl[1] == curr_col}

        if len(candidates) == 0:
            raise Exception("That's weird")

        curr_tpl = sorted(list(candidates))[0]
        cur_row, cur_col, d_row, d_col, steps_in_direction = curr_tpl

        if (d_row, d_col) != (-1, -1):
            if (d_row, d_col) == (0, 1):
                g[cur_row][cur_col] = ">"
            elif (d_row, d_col) == (1, 0):
                g[cur_row][cur_col] = "v"
            elif (d_row, d_col) == (0, -1):
                g[cur_row][cur_col] = "<"
            elif (d_row, d_col) == (-1, 0):
                g[cur_row][cur_col] = "^"
            else:
                raise Exception("That's weird")

        prev_coord = (cur_row - d_row, cur_col - d_col)
        curr_coord = prev_coord

    for row in g:
        print("".join(row))


def part1(grid: Grid):
    heat_loss = search(grid)
    print("Part 1:", heat_loss)


def part2(grid: Grid):
    print("Part 2:", -1)


filename = "day17/example"
filename = "day17/input"

grid = parse(filename)
part1(grid)
# part2(grid)
