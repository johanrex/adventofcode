from collections import deque
from dataclasses import dataclass
import math
from enum import Enum
import copy

Grid = list[list[str]]


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


@dataclass
class TileInfo:
    row: int
    col: int
    light_from: Direction

    def __hash__(self):
        return hash((self.row, self.col, self.light_from))

    def __eq__(self, other):
        if isinstance(other, TileInfo):
            return (
                self.row == other.row
                and self.col == other.col
                and self.light_from == other.light_from
            )
        return False


def parse(filename) -> Grid:
    grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            grid.append([c for c in line])

    return grid


def print_energized(grid: Grid, tile_infos: set[TileInfo]):
    g = copy.deepcopy(grid)
    for t in tile_infos:
        g[t.row][t.col] = "#"

    for row in g:
        print("".join(row))


def invert_direction(direction: Direction) -> Direction:
    if direction == Direction.UP:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.UP
    elif direction == Direction.LEFT:
        return Direction.RIGHT
    elif direction == Direction.RIGHT:
        return Direction.LEFT

    raise Exception(f"Invalid direction: {direction}")


def mirror_direction(direction_from: Direction, mirror: str) -> Direction:
    assert mirror in ("\\", "/")

    if mirror == "/":
        if direction_from == Direction.UP:
            return Direction.LEFT
        elif direction_from == Direction.DOWN:
            return Direction.RIGHT
        elif direction_from == Direction.LEFT:
            return Direction.UP
        elif direction_from == Direction.RIGHT:
            return Direction.DOWN
    elif mirror == "\\":
        if direction_from == Direction.UP:
            return Direction.RIGHT
        elif direction_from == Direction.DOWN:
            return Direction.LEFT
        elif direction_from == Direction.LEFT:
            return Direction.DOWN
        elif direction_from == Direction.RIGHT:
            return Direction.UP

    raise Exception(f"Invalid direction: {direction_from}")


def split_direction(direction_from: Direction) -> tuple[Direction, Direction]:
    if direction_from == Direction.UP or direction_from == Direction.DOWN:
        return Direction.LEFT, Direction.RIGHT
    elif direction_from == Direction.LEFT or direction_from == Direction.RIGHT:
        return Direction.UP, Direction.DOWN

    raise Exception(f"Invalid direction: {direction_from}")


def add_tuples(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


def next_tile(grid: Grid, curr: TileInfo) -> list[TileInfo]:
    next_tiles: list[TileInfo] = []

    if (
        curr.light_from in (Direction.LEFT, Direction.RIGHT)
        and (grid[curr.row][curr.col] in [".", "-"])
    ) or (
        curr.light_from in (Direction.UP, Direction.DOWN)
        and (grid[curr.row][curr.col] in [".", "|"])
    ):
        next_tiles.append(
            TileInfo(
                *add_tuples(
                    (curr.row, curr.col), invert_direction(curr.light_from).value
                ),
                curr.light_from,
            )
        )
    elif grid[curr.row][curr.col] in ("\\", "/"):
        new_d = mirror_direction(curr.light_from, grid[curr.row][curr.col])
        next_tiles.append(
            TileInfo(
                *add_tuples(
                    (curr.row, curr.col),
                    new_d.value,
                ),
                invert_direction(new_d),
            )
        )
    elif (
        curr.light_from in (Direction.LEFT, Direction.RIGHT)
        and (grid[curr.row][curr.col] == "|")
    ) or (
        curr.light_from in (Direction.UP, Direction.DOWN)
        and (grid[curr.row][curr.col] == "-")
    ):
        for d in split_direction(curr.light_from):
            next_tiles.append(
                TileInfo(
                    *add_tuples((curr.row, curr.col), d.value),
                    invert_direction(d),
                )
            )

    # prune out of bounds
    next_tiles = [
        t for t in next_tiles if 0 <= t.row < len(grid) and 0 <= t.col < len(grid[0])
    ]

    return next_tiles


def shine(grid: Grid, start_tile: TileInfo) -> set[TileInfo]:
    visited: set[TileInfo] = set()
    q = deque([start_tile])

    while q:
        curr = q.popleft()

        if curr in visited:
            continue

        visited.add(curr)

        # print("curr:", curr)
        # print_energized(grid, visited)

        next_tiles = next_tile(grid, curr)
        q.extend(next_tiles)

    return visited


def find_energized(grid: Grid, start_tile: TileInfo) -> int:
    tile_infos = shine(grid, start_tile)
    n = len(set([(t.row, t.col) for t in tile_infos]))
    return n


def part1(grid: Grid):
    start_tile = TileInfo(row=0, col=0, light_from=Direction.LEFT)
    n = find_energized(grid, start_tile)

    print("Part 1:", n)


def part2(grid: Grid):
    start_tiles: list[TileInfo] = []

    for row in range(len(grid)):
        start_tiles.append(TileInfo(row=row, col=0, light_from=Direction.LEFT))
        start_tiles.append(
            TileInfo(row=row, col=len(grid[0]) - 1, light_from=Direction.RIGHT)
        )
    for col in range(len(grid[0])):
        start_tiles.append(TileInfo(row=0, col=col, light_from=Direction.UP))
        start_tiles.append(
            TileInfo(row=len(grid) - 1, col=col, light_from=Direction.DOWN)
        )

    max_energy = 0
    for t in start_tiles:
        max_energy = max(max_energy, find_energized(grid, t))
    print("Part 2:", max_energy)


# filename = "day16/example"
filename = "day16/input"

grid = parse(filename)
# part1(grid)
part2(grid)
