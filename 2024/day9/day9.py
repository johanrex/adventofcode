DiskMap = list[int]
Layout = list[str]


def parse(filename: str) -> DiskMap:
    with open(filename) as f:
        s = f.read().strip()
        disk_map = list(map(int, [c for c in s]))
    return disk_map


def expand(disk_map: DiskMap) -> Layout:
    layout = []
    file_id = 0

    for i in range(len(disk_map)):
        if i % 2 == 0:
            layout.extend([str(file_id)] * disk_map[i])
            file_id += 1
        else:
            layout.extend(["."] * disk_map[i])
    return layout


def compact(layout: Layout) -> Layout:
    lo = 0
    hi = len(layout) - 1

    while True:
        while layout[lo] != ".":
            lo += 1

        while layout[hi] == ".":
            hi -= 1

        if lo >= hi:
            break

        # swap
        layout[lo], layout[hi] = layout[hi], layout[lo]

    return layout


def checksum(layout: Layout) -> int:
    s = 0
    for i in range(len(layout)):
        if layout[i] == ".":
            continue
        file_id = int(layout[i])
        s += file_id * i
    return s


def part1(disk_map: DiskMap):
    print("disk_map")
    print(disk_map)

    layout = expand(disk_map)

    print("layout before compact")
    print(layout)

    layout = compact(layout)

    print("layout after compact")
    print(layout)

    s = checksum(layout)
    # 6349606729700 too high
    print("Part 1:", s)


def part2(disk_map: DiskMap):
    print("Part 2:", -1)


# filename = "day9/example"
filename = "day9/input"

disk_map = parse(filename)
part1(disk_map)
