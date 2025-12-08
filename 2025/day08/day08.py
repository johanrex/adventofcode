from dataclasses import dataclass
import math


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
        connection_cnt = 10
    else:  # is real input
        connection_cnt = 1000

    p1_ans = 0
    p2_ans = 0

    # cliques, init with all points separate
    cliques = [set([p]) for p in points]

    # make connections
    for i in range(len(dists)):
        d, (p1, p2) = dists[i]

        # find clique for p1
        for j, c1 in enumerate(cliques):
            if p1 in c1:
                break

        # find clique for p2
        for k, c2 in enumerate(cliques):
            if p2 in c2:
                break

        if j == k:
            continue  # already in same clique. Nothing to do

        # we have two cliques that should be merged.

        min_idx = min(j, k)
        max_idx = max(j, k)

        # pop the later clique to keep indices valid
        later_clique = cliques.pop(max_idx)

        # merge into the other clique
        cliques[min_idx] = cliques[min_idx] | later_clique

        if i == connection_cnt:
            sizes = [len(c) for c in cliques]
            sizes.sort(reverse=True)
            p1_ans = math.prod(sizes[:3])

        p2_ans = p1.x * p2.x

    assert p1_ans == 97384
    print("Part 1:", p1_ans)

    assert p2_ans == 9003685096
    print("Part 2:", p2_ans)


# filename = "day08/example"
filename = "day08/input"

points = parse(filename)
solve(points)
