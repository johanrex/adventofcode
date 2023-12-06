from dataclasses import dataclass
import math


@dataclass
class Race:
    time: int
    distance: int


def parse(filename):
    times = []
    distances = []
    with open(filename) as f:
        line = f.readline().strip()
        line = line.replace("Time:      ", "")
        times = [int(x) for x in line.split()]

        line = f.readline().strip()
        line = line.replace("Distance:  ", "")
        distances = [int(x) for x in line.split()]
    return times, distances


def part1(times, distances):
    record_cnts = []
    for time, max_distance in zip(times, distances):
        record_cnt = 0
        for t in range(time + 1):
            velocity = t
            remaining = time - t
            distance = velocity * remaining
            if distance > max_distance:
                record_cnt += 1
        record_cnts.append(record_cnt)

    p = math.prod(record_cnts)
    print("Part 1:", p)


def part2(times, distances):
    time = int("".join([str(t) for t in times]))
    max_distance = int("".join([str(d) for d in distances]))

    record_cnt = 0
    for t in range(time + 1):
        velocity = t
        remaining = time - t
        distance = velocity * remaining
        if distance > max_distance:
            record_cnt += 1

    print("Part 2:", record_cnt)


# filename = "6/example"
filename = "6/input"

times, distances = parse(filename)
part1(times, distances)
part2(times, distances)
