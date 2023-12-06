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
        # print(time, max_distance)
        record_cnt = 0
        for t in range(time + 1):
            velocity = t
            remaining = time - t
            distance = velocity * remaining
            # print(t, distance)
            if distance > max_distance:
                record_cnt += 1
        record_cnts.append(record_cnt)

    p = math.prod(record_cnts)
    print("Part 1:", p)


def part2(times, distances):
    race_time = int("".join([str(t) for t in times]))
    race_distance = int("".join([str(d) for d in distances]))

    print(race_time)
    print(race_distance)


filename = "6/example"
# filename = "6/input"

times, distances = parse(filename)
part1(times, distances)
part2(times, distances)
