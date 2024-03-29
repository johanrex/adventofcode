from collections import Counter
import re

pat = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")


def get_distance(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_coords_within_distance_p1(coord: tuple[int, int], distance, row):
    x, y = coord
    coords = set()

    # for x_i in range(x - distance, (x + distance) + 1):

    # for y_i in range(y - distance, (y + distance) + 1):
    y_i = row
    for x_i in range(x - distance, (x + distance) + 1):
        coord_candidate = (x_i, y_i)
        if get_distance(coord, coord_candidate) > distance:
            continue
        else:
            coords.add(coord_candidate)

    return coords


def get_coords_within_distance(coord: tuple[int, int], distance):
    x, y = coord
    coords = set()

    for y_i in range(y - distance, (y + distance) + 1):
        for x_i in range(x - distance, (x + distance) + 1):
            coord_candidate = (x_i, y_i)
            if get_distance(coord, coord_candidate) > distance:
                continue
            else:
                coords.add(coord_candidate)

    return coords


def parse(filename):
    sensor_beacon = {}

    with open(filename) as f:
        for line in f:
            m = re.match(pat, line.strip())
            if m is None:
                raise Exception("")
            sensor = (int(m.group(1)), int(m.group(2)))
            beacon = (int(m.group(3)), int(m.group(4)))
            sensor_beacon[sensor] = beacon

    return sensor_beacon


def part1(sensor_beacon):
    row = 2000000
    visible_coords_at_row = set()
    sensors = sensor_beacon.keys()
    for sensor, beacon in sensor_beacon.items():
        d = get_distance(sensor, beacon)
        coords = get_coords_within_distance_p1(sensor, d, row)
        # coords = [coord for coord in coords if coord[1] == row]

        visible_coords_at_row |= coords

    for sensor, beacon in sensor_beacon.items():
        if sensor in visible_coords_at_row:
            visible_coords_at_row.remove(sensor)
        if beacon in visible_coords_at_row:
            visible_coords_at_row.remove(beacon)

    return len(visible_coords_at_row)


def part2(sensor_beacon: dict[tuple[int, int], tuple[int, int]]):
    pass
    # TODO for each sensor, find all coords one step outside of the diamond. The do set.intersection on all those to find the single point.

    # c_all = Counter()
    # l_bound = 0
    # u_bound = 4_000_000

    # for sensor, beacon in sensor_beacon.items():
    #     d_plus_one = get_distance(sensor, beacon) + 1
    #     coords = get_coords_within_distance(sensor, d_plus_one)
    #     coords = {coord for coord in coords if (l_bound <= coord[0] <= u_bound) and (l_bound <= coord[1] <= u_bound)}
    #     c = Counter(coords)

    #     pass


# filename = "15/example"
filename = "15/input"
sensor_beacon = parse(filename)

# p1 = part1(sensor_beacon)
# assert p1 == 5403290
# print("Part1:", p1)

# TODO
part2(sensor_beacon)
pass
