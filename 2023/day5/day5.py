from dataclasses import dataclass
import sys
from multiprocessing import Pool


@dataclass
class Map:
    dst_start: int
    dst_end: int
    src_start: int
    src_end: int


def parse(filename: str) -> tuple[list[int], list[list[Map]]]:
    def get_section_map(prefix: str) -> list[Map]:
        line = f.readline().strip()
        maps = []

        if prefix not in line:
            raise ValueError("Unexpected line: " + line)

        line = f.readline().strip()
        while line != "":
            line = line.strip()
            line = line.replace(prefix, "")
            tokens_str = line.split()
            tokens = [int(token) for token in tokens_str]
            dst = tokens[0]
            src = tokens[1]
            length = tokens[2]

            maps.append(Map(dst, dst + length - 1, src, src + length - 1))

            line = f.readline().strip()
        return maps

    category_maps = []
    with open(filename) as f:
        line = f.readline().strip()
        prefix = "seeds: "
        if prefix not in line:
            raise ValueError("Unexpected line: " + line)
        line = line.replace(prefix, "")
        seeds_str = line.split()
        seeds = [int(seed) for seed in seeds_str]
        line = f.readline().strip()
        assert "" == line

        category_maps.append(get_section_map("seed-to-soil map:"))
        category_maps.append(get_section_map("soil-to-fertilizer map:"))
        category_maps.append(get_section_map("fertilizer-to-water map:"))
        category_maps.append(get_section_map("water-to-light map:"))
        category_maps.append(get_section_map("light-to-temperature map:"))
        category_maps.append(get_section_map("temperature-to-humidity map:"))
        category_maps.append(get_section_map("humidity-to-location map:"))

    return seeds, category_maps


def map_seed(seed: int, category_maps: list[list[Map]]) -> int:
    val = seed

    for category_map in category_maps:
        for cm in category_map:
            if cm.src_start <= val <= cm.src_end:
                offset = val - cm.src_start
                val = cm.dst_start + offset
                break
    return val


def part1(seeds: list[int], category_maps: list[list[Map]]) -> None:
    location_nrs = []
    for seed in seeds:
        val = map_seed(seed, category_maps)
        location_nrs.append(val)

    print("Part1:", min(location_nrs))


def eval_range(seed_range: range, category_maps: list[list[Map]]) -> int:
    min_location_nr = sys.maxsize
    location_nrs = []
    for seed in seed_range:
        val = map_seed(seed, category_maps)
        min_location_nr = min(min_location_nr, val)
        location_nrs.append(val)

    return min_location_nr


def eval_wrapper(args: tuple[range, list[list[Map]]]):
    return eval_range(*args)


def part2(seed_range_info: list[int], category_maps: list[list[Map]]) -> None:
    seed_ranges = []

    for i in range(0, len(seed_range_info), 2):
        seed_start = seed_range_info[i]
        nr_seeds = seed_range_info[i + 1]

        seed_end = seed_start + nr_seeds - 1

        seed_range = range(seed_start, seed_end + 1)
        seed_ranges.append(seed_range)

    with Pool() as p:
        min_range_vals = p.map(
            eval_wrapper, [(seed_range, category_maps) for seed_range in seed_ranges]
        )

    print("Part2:", min(min_range_vals))


if __name__ == "__main__":
    filename = "5/example"
    # filename = "5/input"
    seeds, category_maps = parse(filename)
    part1(seeds, category_maps)
    part2(seeds, category_maps)
