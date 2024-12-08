import math
import re
import copy
from collections import Counter, defaultdict
from itertools import combinations

Grid = list[list[str]]
Antennas = dict[str, list[tuple[int, int]]]
Antinodes = set[tuple[int, int]]


def parse(filename: str) -> tuple[Grid, Antennas]:
    grid = []
    with open(filename) as f:
        for line in f:
            grid.append([c for c in line.strip()])

    antennas = defaultdict(list)
    for r in range(len(grid)):
        row = grid[r]
        for c in range(len(row)):
            char = row[c]
            if char != ".":
                antennas[char].append((r, c))

    return grid, antennas


def print_grid(grid: Grid, antinodes: Antinodes = None):
    grid = copy.deepcopy(grid)

    if antinodes:
        for antinode in antinodes:
            r, c = antinode
            grid[r][c] = "#"

    for r in range(len(grid)):
        row = grid[r]
        print("".join(row))


def part1(grid: Grid, antennas: Antennas):
    antinodes: Antinodes = set()

    for freq in antennas.keys():
        positions = antennas[freq]

        list_of_pairs = list(combinations(positions, 2))
        print(f"{freq}: {list_of_pairs}")

        for pair in list_of_pairs:
            a1, a2 = pair

            dr = a1[0] - a2[0]
            dc = a1[1] - a2[1]

            antinode_1 = (a1[0] + dr, a1[1] + dc)
            antinode_2 = (a2[0] - dr, a2[1] - dc)

            if (0 <= antinode_1[0] < len(grid)) and (0 <= antinode_1[1] < len(grid[0])):
                antinodes.add(antinode_1)
            if (0 <= antinode_2[0] < len(grid)) and (0 <= antinode_2[1] < len(grid[0])):
                antinodes.add(antinode_2)

    print_grid(grid, antinodes)
    s = len(antinodes)
    assert s == 259
    print("Part 1:", s)


def part2(grid: Grid):
    print("Part 2:", -1)


# filename = "day8/example"
filename = "day8/input"

grid, antennas = parse(filename)
# print_grid(grid)

part1(grid, antennas)
# part2(grid)
