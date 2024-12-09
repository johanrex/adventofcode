from dataclasses import dataclass


@dataclass
class DiskRegion:
    block_start: int
    block_end: int
    file_id: int


DiskMap = list[int]
Layout = list[str]
DiskRegions = list[DiskRegion]


def parse(filename: str) -> DiskMap:
    with open(filename) as f:
        s = f.read().strip()
        disk_map = list(map(int, [c for c in s]))
    return disk_map


def diskmap_to_layout(disk_map: DiskMap) -> Layout:
    layout = []
    file_id = 0

    for i in range(len(disk_map)):
        if i % 2 == 0:
            layout.extend([str(file_id)] * disk_map[i])
            file_id += 1
        else:
            layout.extend(["."] * disk_map[i])
    return layout


def diskregions_to_string(disk_regions: DiskRegions) -> str:
    s = ""
    for region in disk_regions:
        region_size = region.block_end - region.block_start
        if region.file_id == -1:
            s += "." * region_size
        else:
            s += str(region.file_id) * region_size
    return s


def compact1(layout: Layout) -> Layout:
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


def checksum1(layout: Layout) -> int:
    s = 0
    for i in range(len(layout)):
        if layout[i] == ".":
            continue
        file_id = int(layout[i])
        s += file_id * i
    return s


def diskmap_to_diskregions(disk_map: DiskMap) -> DiskRegions:
    disk_regions = []

    file_id = 0
    file_count = 0
    cum_pos = 0
    for i in range(len(disk_map)):
        if i % 2 == 0:
            file_id = file_count
        else:
            # -1 for empty space
            file_id = -1

        region_size = disk_map[i]

        region = DiskRegion(block_start=cum_pos, block_end=cum_pos + region_size, file_id=file_id)
        disk_regions.append(region)

        cum_pos += region_size

        if i % 2 == 0:
            file_count += 1

    return disk_regions


def compact2(disk_regions: DiskRegions) -> DiskRegions:
    pass


def part1(disk_map: DiskMap):
    layout = diskmap_to_layout(disk_map)
    layout = compact1(layout)
    s = checksum1(layout)

    print(layout)

    # assert s == 6349606724455
    print("Part 1:", s)


def part2(disk_map: DiskMap):
    disk_regions = diskmap_to_diskregions(disk_map)
    print(disk_regions)
    print(diskregions_to_string(disk_regions))

    print("Part 2:", -1)


filename = "day9/example"
# filename = "day9/input"

disk_map = parse(filename)
part1(disk_map)
part2(disk_map)
