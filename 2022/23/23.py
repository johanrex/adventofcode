from enum import Enum
import numpy as np


class Direction(Enum):
    north = 1
    north_east = 2
    east = 3
    south_east = 4
    south = 5
    south_west = 6
    west = 7
    north_west = 8


def parse(filename) -> np.ndarray:
    with open(filename) as f:
        lines = f.readlines()
        lines = [list(line.strip()) for line in lines]

    grid = np.array(lines)
    return grid


def directions_to_consider_generator():
    i = 0
    direction_cycle = [Direction.north, Direction.south, Direction.west, Direction.east]

    while True:
        a = direction_cycle[i % len(direction_cycle)]
        b = direction_cycle[(i + 1) % len(direction_cycle)]
        c = direction_cycle[(i + 2) % len(direction_cycle)]
        d = direction_cycle[(i + 3) % len(direction_cycle)]

        yield [a, b, c, d]
        i += 1


def prune_grid(grid):
    while not any(grid[0] == "#"):
        grid = np.delete(grid, 0, axis=0)

    while not any(grid[-1] == "#"):
        grid = np.delete(grid, -1, axis=0)

    while not any(grid[:, 0] == "#"):
        grid = np.delete(grid, 0, axis=1)

    while not any(grid[:, -1] == "#"):
        grid = np.delete(grid, -1, axis=1)

    return grid


def ensure_grid_has_room_to_move(grid: np.ndarray):
    # any elf on first row?
    if any(grid[0] == "#"):
        grid = np.insert(grid, 0, ["."] * grid.shape[1], axis=0)

    # any elf on last row?
    if any(grid[-1] == "#"):
        grid = np.insert(grid, grid.shape[0], ["."] * grid.shape[1], axis=0)

    # any elf on first col?
    if any(grid[:, 0] == "#"):
        grid = np.insert(grid, 0, ["."] * grid.shape[0], axis=1)

    # any elf on last col?
    if any(grid[:, -1] == "#"):
        grid = np.insert(grid, grid.shape[1], ["."] * grid.shape[0], axis=1)

    return grid


def do_round(grid: np.ndarray, directions_to_consider: list[Direction]):

    grid = ensure_grid_has_room_to_move(grid)
    rows = grid.shape[0]
    cols = grid.shape[1]

    nr_elves_moved = 0

    # (row_old, col_old, row_new, col_new)
    move_proposals = []
    for curr_row in range(1, rows - 1):
        for curr_col in range(1, cols - 1):
            if grid[curr_row][curr_col] == "#":
                # should move at all? check all directions.
                north_free = grid[curr_row - 1][curr_col] == "."
                north_east_free = grid[curr_row - 1][curr_col + 1] == "."
                east_free = grid[curr_row][curr_col + 1] == "."
                south_east_free = grid[curr_row + 1][curr_col + 1] == "."
                south_free = grid[curr_row + 1][curr_col] == "."
                south_west_free = grid[curr_row + 1][curr_col - 1] == "."
                west_free = grid[curr_row][curr_col - 1] == "."
                north_west_free = grid[curr_row - 1][curr_col - 1] == "."

                if (
                    north_free
                    and north_east_free
                    and east_free
                    and south_east_free
                    and south_free
                    and south_west_free
                    and west_free
                    and north_west_free
                ):
                    # stay put
                    pass
                else:
                    for direction in directions_to_consider:
                        if direction == Direction.north:
                            if north_west_free and north_free and north_east_free:
                                move_proposals.append((curr_row, curr_col, curr_row - 1, curr_col))
                                break
                        elif direction == Direction.south:
                            if south_west_free and south_free and south_east_free:
                                move_proposals.append((curr_row, curr_col, curr_row + 1, curr_col))
                                break
                        elif direction == Direction.west:
                            if north_west_free and west_free and south_west_free:
                                move_proposals.append((curr_row, curr_col, curr_row, curr_col - 1))
                                break
                        elif direction == Direction.east:
                            if north_east_free and east_free and south_east_free:
                                move_proposals.append((curr_row, curr_col, curr_row, curr_col + 1))
                                break

    # evaluate proposals
    # TODO could be optimized by sorting first
    # (row_old, col_old, row_new, col_new)
    for move_proposal in move_proposals:
        old_row, old_col, new_row, new_col = move_proposal

        # horrible
        is_unique_proposal = (
            len(
                [
                    (other_old_row, other_old_col, other_new_row, other_new_col)
                    for other_old_row, other_old_col, other_new_row, other_new_col in move_proposals
                    if other_new_row == new_row and other_new_col == new_col
                ]
            )
            == 1
        )

        if is_unique_proposal:
            # do the move
            assert grid[old_row][old_col] == "#"
            assert grid[new_row][new_col] == "."

            grid[old_row][old_col] = "."
            grid[new_row][new_col] = "#"

            nr_elves_moved += 1

    return grid, nr_elves_moved


def print_grid(grid: np.ndarray):
    for row in grid:
        print("".join(row))


# filename = "23/example"
filename = "23/input"
grid = parse(filename)

direction_to_consider_gen = directions_to_consider_generator()

print("Initial state:")
print_grid(grid)

round = 0
while True:
    directions_to_consider = next(direction_to_consider_gen)
    grid, nr_elves_moved = do_round(grid, directions_to_consider)

    round += 1

    if round == 10:
        # print(f"After round {i+1}:")
        # print_grid(grid)

        print("Part1:", np.sum(prune_grid(grid) == "."))

    if nr_elves_moved == 0:
        print("Part2:", round)
        break


pass
