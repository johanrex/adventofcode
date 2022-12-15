import re

pat = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")


def get_distance(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_coords_within_distance(coord: tuple[int, int], distance):
    x, y = coord
    coords = []

    # for x_i in range(x - distance, (x + distance) + 1):

    for y_i in range(y - distance, (y + distance) + 1):
        for x_i in range(x - distance, (x + distance) + 1):
            coord_candidate = (x_i, y_i)
            if get_distance(coord, coord_candidate) > distance:
                continue
            else:
                coords.append(coord_candidate)

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


# print(sensors)
# print(beacons)

# filename = "15/example"
filename = "15/input"
sensor_beacon = parse(filename)

# sensor = (8, 7)
# beacon = (2, 10)
# d = get_distance(sensor, beacon)

# coords = get_coords_within_distance(sensor, d)

row = 10
visible_coords_at_row = set()
sensors = sensor_beacon.keys()
for sensor, beacon in sensor_beacon.items():
    d = get_distance(sensor, beacon)
    coords = get_coords_within_distance(sensor, d)
    coords = [coord for coord in coords if coord[1] == row]

    visible_coords_at_row |= set(coords)

for sensor, beacon in sensor_beacon.items():
    if sensor in visible_coords_at_row:
        visible_coords_at_row.remove(sensor)
    if beacon in visible_coords_at_row:
        visible_coords_at_row.remove(beacon)

print(list(sorted(visible_coords_at_row)))

print("Part1:", len(visible_coords_at_row))
pass
# Find sensor - beacon pairs.
