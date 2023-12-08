import re
import math
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return self.x * 1000 + self.y


@dataclass
class SchematicObject:
    point: Point
    value: str


def get_adjacent_points(obj: SchematicObject, grid):
    max_x = len(grid[0])
    max_y = len(grid)
    adjacent_points = []

    # above
    if obj.point.y > 0:
        start_y = obj.point.y - 1
        start_x = max(obj.point.x - 1, 0)
        stop_x = min(obj.point.x + len(obj.value), max_x)
        for x in range(start_x, stop_x + 1):
            p = Point(x, start_y)
            adjacent_points.append(p)

    # below
    if obj.point.y < max_y - 1:
        start_y = obj.point.y + 1
        start_x = max(obj.point.x - 1, 0)
        stop_x = min(obj.point.x + len(obj.value), max_x)
        for x in range(start_x, stop_x + 1):
            p = Point(x, start_y)
            adjacent_points.append(p)

    # left
    if obj.point.x > 0:
        adjacent_points.append(Point(obj.point.x - 1, obj.point.y))

    # right
    if obj.point.x < max_x - 1:
        adjacent_points.append(Point(obj.point.x + len(obj.value), obj.point.y))

    return adjacent_points


def get_schematic_pattern(grid, pattern):
    lst = []
    for row, line in enumerate(grid):
        for m in pattern.finditer(line):
            lst.append(SchematicObject(Point(m.start(), row), m.group(0)))
    return lst


def get_part_nrs(grid):
    pat_symbols = re.compile(r"[^\d\.]")
    symbols = get_schematic_pattern(grid, pat_symbols)

    pat_nrs = re.compile(r"(\d+)")
    nrs = get_schematic_pattern(grid, pat_nrs)

    part_nrs = []
    for nr in nrs:
        added = False
        adjacent_points = get_adjacent_points(nr, grid)
        # is there a symbol in any of the adjacent points?
        for p in adjacent_points:
            for symbol in symbols:
                if p.x == symbol.point.x and p.y == symbol.point.y:
                    part_nrs.append(nr)
                    added = True
                    break
            if added:
                break

    return part_nrs


def part1(grid):
    part_nrs = get_part_nrs(grid)
    nrs = [int(nr.value) for nr in part_nrs]
    s = sum(nrs)
    assert 533775 == s
    print("Part 1:", s)


def nr_covering_points(nr):
    points = []
    for x in range(nr.point.x, nr.point.x + len(nr.value)):
        points.append(Point(x, nr.point.y))
    return points


def part2(grid):
    pat_gears = re.compile(r"\*")
    gear_candidates = get_schematic_pattern(grid, pat_gears)

    part_nrs = get_part_nrs(grid)

    gear_ratios = []
    for gear_candidate in gear_candidates:
        adjacent_points = get_adjacent_points(gear_candidate, grid)

        is_adjacent_to_part_nrs = []

        for part_nr in part_nrs:
            part_nr_points = nr_covering_points(part_nr)
            if len(set(adjacent_points).intersection(set(part_nr_points))) > 0:
                is_adjacent_to_part_nrs.append(int(part_nr.value))

                if len(is_adjacent_to_part_nrs) > 2:
                    break

        if len(is_adjacent_to_part_nrs) == 2:
            gear_ratio = math.prod(is_adjacent_to_part_nrs)
            gear_ratios.append(gear_ratio)

    s = sum(gear_ratios)
    assert 78236071 == s
    print("Part 2:", s)


# filename = "3/example"
filename = "3/input"
with open(filename) as f:
    grid = [line.strip() for line in f.readlines()]


part1(grid)
part2(grid)
