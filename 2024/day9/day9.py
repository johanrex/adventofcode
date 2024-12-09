from dataclasses import dataclass
from heapq import heappush, heappop, heapify


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


def print_diskregions(disk_regions: DiskRegions):
    s = ""
    for region in disk_regions:
        region_size = region.block_end - region.block_start
        if region.file_id == -1:
            s += "." * region_size
        else:
            s += str(region.file_id) * region_size
    print(s)


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


def checksum2(disk_regions: DiskRegions) -> int:
    s = 0
    block_id = 0
    for region in disk_regions:
        if region.file_id == -1:
            block_id += region.block_end - region.block_start
            continue

        for _ in range(region.block_start, region.block_end):
            s += region.file_id * block_id
            block_id += 1

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


def compact2_inplace(disk_regions: DiskRegions) -> DiskRegions:
    attempted_file_ids = set()

    assert disk_regions[0].file_id != -1

    while True:
        if disk_regions[0].file_id in attempted_file_ids:
            break

        # find last file that has not been attempted before.
        src_file = None
        for hi in range(len(disk_regions) - 1, -1, -1):
            if disk_regions[hi].file_id != -1 and disk_regions[hi].file_id not in attempted_file_ids:
                src_file = disk_regions[hi]
                attempted_file_ids.add(src_file.file_id)
                break
            hi -= 1

        if src_file is None:
            break

        src_file_size = src_file.block_end - src_file.block_start

        # find first empty space that can fit the file
        dst_free_region = None
        for lo in range(len(disk_regions)):
            if disk_regions[lo].file_id == -1 and disk_regions[lo].block_end - disk_regions[lo].block_start >= src_file_size:
                dst_free_region = disk_regions[lo]
                break

        if dst_free_region is None:
            continue

        if lo >= hi:
            continue

        dst_free_region_size = dst_free_region.block_end - dst_free_region.block_start

        # file fits perfectly
        if dst_free_region_size == src_file_size:
            dst_free_region.file_id = src_file.file_id
            src_file.file_id = -1
        else:
            # we get some free space after the file
            assert dst_free_region_size > src_file_size

            # create new file object and insert it before the free space
            file_in_transit = DiskRegion(src_file.block_start, src_file.block_end, src_file.file_id)
            file_in_transit.block_start = dst_free_region.block_start
            file_in_transit.block_end = dst_free_region.block_start + src_file_size
            disk_regions.insert(lo, file_in_transit)

            # subtract file size from free space
            dst_free_region.block_start += src_file_size

            # remove the original file (mark as empty space)
            src_file.file_id = -1

        # print(diskregions_to_string(disk_regions))
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

    compact2_inplace(disk_regions)

    s = checksum2(disk_regions)

    # 85900447205 too low
    print("Part 2:", s)


# filename = "day9/example"
filename = "day9/input"

disk_map = parse(filename)
part1(disk_map)
part2(disk_map)
