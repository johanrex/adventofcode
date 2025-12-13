from dataclasses import dataclass
import math
import os
import sys

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from utils.union_find import UnionFind


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)


def parse(filename: str) -> list[Point]:
    points = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            nrs = line.split(",")
            points.append(Point(int(nrs[0]), int(nrs[1]), int(nrs[2])))

    return points


def solve(points: list[Point]):
    # sort points so we can translate to 0-based indeces for union-find
    points.sort()

    # need to translate point to idx for union-find
    point_to_idx = {points[i]: i for i in range(len(points))}

    # calculate all pairwise distances
    dists = []
    for i in range(len(points)):
        p1 = points[i]
        for j in range(i + 1, len(points)):
            p2 = points[j]

            d = (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2
            dists.append((d, (p1, p2)))
    dists.sort()

    # how many connections to make
    if len(points) == 20:  # is example
        connections_to_make = 10
    else:  # is real input
        connections_to_make = 1000

    p1_ans = 0
    p2_ans = 0

    # let's make connections
    uf = UnionFind(len(points))
    for i in range(len(dists)):
        d, (p1, p2) = dists[i]

        p1_idx = point_to_idx[p1]
        p2_idx = point_to_idx[p2]

        # find the representative roots
        r1 = uf.find(p1_idx)
        r2 = uf.find(p2_idx)

        # union sets, if they are disjoint
        union_performed = uf.union(r1, r2)
        if union_performed:
            p2_ans = p1.x * p2.x

        if i + 1 == connections_to_make:
            p1_ans = math.prod(sorted(uf.size, reverse=True)[:3])

    assert p1_ans == 97384
    print("Part 1:", p1_ans)

    assert p2_ans == 9003685096
    print("Part 2:", p2_ans)


# filename = "day08/example"
filename = "day08/input"

points = parse(filename)
solve(points)
