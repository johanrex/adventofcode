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
        connections_to_make = 10
    else:  # is real input
        connections_to_make = 1000

    p1_ans = 0
    p2_ans = 0

    # disjoint sets, init with all points separate
    disjoint_sets = [set([p]) for p in points]

    # make connections
    for i in range(len(dists)):
        d, (p1, p2) = dists[i]

        # find set for p1
        for j, s1 in enumerate(disjoint_sets):
            if p1 in s1:
                break

        # find set for p2
        for k, s2 in enumerate(disjoint_sets):
            if p2 in s2:
                break

        if j != k:
            # we have two disjoint sets that should be merged.

            min_idx = min(j, k)
            max_idx = max(j, k)

            # pop the later set to keep indices valid
            later_set = disjoint_sets.pop(max_idx)

            # merge into the other set
            disjoint_sets[min_idx] = disjoint_sets[min_idx] | later_set

            p2_ans = p1.x * p2.x

        if i + 1 == connections_to_make:
            sizes = [len(c) for c in disjoint_sets]
            sizes.sort(reverse=True)
            p1_ans = math.prod(sizes[:3])

    assert p1_ans == 97384
    print("Part 1:", p1_ans)

    assert p2_ans == 9003685096
    print("Part 2:", p2_ans)


# filename = "day08/example"
filename = "day08/input"

points = parse(filename)
solve(points)
