from dataclasses import dataclass
import sys
from typing import Self


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __cmp(self, other: Self):
        if self.x < other.x:
            return -1
        elif self.x > other.x:
            return 1
        else:
            if self.y < other.y:
                return -1
            elif self.y > other.y:
                return 1
            else:
                if self.z < other.z:
                    return -1
                elif self.z > other.z:
                    return 1
                else:
                    return 0

    def __lt__(self, other):
        return self.__cmp(other) < 0

    def __le__(self, other):
        return self.__cmp(other) <= 0

    def __eq__(self, other):
        return self.__cmp(other) == 0

    def __ne__(self, other):
        return self.__cmp(other) != 0

    def __gt__(self, other):
        return self.__cmp(other) > 0

    def __ge__(self, other):
        return self.__cmp(other) >= 0


def parse(filename):
    points = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            vals = list(map(int, line.split(",")))
            c = Point(vals[0], vals[1], vals[2])
            points.append(c)
    return points


def get_visible_sides(points):

    side_cnt = 0

    for p1 in points:
        # left
        if next((p2 for p2 in points if p1.x - 1 == p2.x and p1.y == p2.y and p1.z == p2.z), None) is None:
            side_cnt += 1

        # right
        if next((p2 for p2 in points if p1.x + 1 == p2.x and p1.y == p2.y and p1.z == p2.z), None) is None:
            side_cnt += 1

        # up
        if next((p2 for p2 in points if p1.x == p2.x and p1.y + 1 == p2.y and p1.z == p2.z), None) is None:
            side_cnt += 1

        # down
        if next((p2 for p2 in points if p1.x == p2.x and p1.y - 1 == p2.y and p1.z == p2.z), None) is None:
            side_cnt += 1

        # front
        if next((p2 for p2 in points if p1.x == p2.x and p1.y == p2.y and p1.z + 1 == p2.z), None) is None:
            side_cnt += 1

        # back
        if next((p2 for p2 in points if p1.x == p2.x and p1.y == p2.y and p1.z - 1 == p2.z), None) is None:
            side_cnt += 1

    return side_cnt


def get_enclosing_points(points):

    min_x = min_y = min_z = sys.maxsize
    max_x = max_y = max_z = -sys.maxsize

    for p in points:
        min_x = min(min_x, p.x)
        min_y = min(min_y, p.y)
        min_z = min(min_z, p.z)

        max_x = max(max_x, p.x)
        max_y = max(max_y, p.y)
        max_z = max(max_z, p.z)

    return Point(min_x - 1, min_y - 1, min_z - 1), Point(max_x + 1, max_y + 1, max_z + 1)


def get_neighbors(p: Point, min_p: Point, max_p: Point) -> set[Point]:
    ns = set()
    if p.x - 1 >= min_p.x:
        ns.add(Point(p.x - 1, p.y, p.z))
    if p.x + 1 <= max_p.x:
        ns.add(Point(p.x + 1, p.y, p.z))
    if p.y - 1 >= min_p.y:
        ns.add(Point(p.x, p.y - 1, p.z))
    if p.y + 1 <= max_p.y:
        ns.add(Point(p.x, p.y + 1, p.z))
    if p.z - 1 >= min_p.z:
        ns.add(Point(p.x, p.y, p.z - 1))
    if p.z + 1 <= max_p.z:
        ns.add(Point(p.x, p.y, p.z + 1))
    return ns


def bfs(min_p, max_p, points):
    q = [min_p]
    visited = set()
    surface_pairs = set()
    while len(q) > 0:
        p = q.pop()
        visited.add(p)

        visit_candidates = get_neighbors(p, min_p, max_p)

        for n in visit_candidates:
            if n in points:
                surface_pairs.add((p, n))
            else:
                if n not in visited:
                    q.append(n)

    return len(surface_pairs)


# filename = "18/example"
filename = "18/input"
points = parse(filename)

sides = get_visible_sides(points)
assert sides == 4504
print("Part1:", sides)

min_p, max_p = get_enclosing_points(points)

surfaces = bfs(min_p, max_p, points)
assert surfaces == 2556
print("Part2:", surfaces)
