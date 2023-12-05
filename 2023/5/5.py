"""
50 98 2
52 50 48

Each line within a map contains three numbers: 
    the destination range start, 
    the source range start, 
    and the range length.

With this information, you know that 
    seed number 98 corresponds to soil number 50 and that 
    seed number 99 corresponds to soil number 51.    

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. 
This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. 
So, seed number 53 corresponds to soil number 55.    

Any source numbers that aren't mapped correspond to the same destination number. 
So, seed number 10 corresponds to soil number 10.


"""

from dataclasses import dataclass


@dataclass
class Map:
    dst_start: int
    dst_end: int
    src_start: int
    src_end: int


def print_maps(maps):
    for map in maps:
        print(map)


def parse(filename):
    def get_section_map(prefix):
        line = f.readline().strip()
        map = []

        if prefix not in line:
            raise ValueError("Unexpected line: " + line)

        line = f.readline().strip()
        while line != "":
            line = line.strip()
            line = line.replace(prefix, "")
            tokens = line.split()
            tokens = [int(token) for token in tokens]
            dst = tokens[0]
            src = tokens[1]
            length = tokens[2]

            map.append(Map(dst, dst + length - 1, src, src + length - 1))

            line = f.readline().strip()
        return map

    category_maps = []
    with open(filename) as f:
        line = f.readline().strip()
        prefix = "seeds: "
        if prefix not in line:
            raise ValueError("Unexpected line: " + line)
        line = line.replace(prefix, "")
        seeds = line.split()
        seeds = [int(seed) for seed in seeds]
        line = f.readline().strip()
        assert "" == line

        seed_to_soil = get_section_map("seed-to-soil map:")
        soil_to_fertilizer = get_section_map("soil-to-fertilizer map:")
        fertilizer_to_water = get_section_map("fertilizer-to-water map:")
        water_to_light = get_section_map("water-to-light map:")
        light_to_temperature = get_section_map("light-to-temperature map:")
        temperature_to_humidity = get_section_map("temperature-to-humidity map:")
        humidity_to_location = get_section_map("humidity-to-location map:")

        category_maps.append(seed_to_soil)
        category_maps.append(soil_to_fertilizer)
        category_maps.append(fertilizer_to_water)
        category_maps.append(water_to_light)
        category_maps.append(light_to_temperature)
        category_maps.append(temperature_to_humidity)
        category_maps.append(humidity_to_location)
    return seeds, category_maps


def part1(seeds, category_maps):
    location_nrs = []
    for seed in seeds:
        val = seed

        for category_map in category_maps:
            for cm in category_map:
                if cm.src_start <= val <= cm.src_end:
                    offset = val - cm.src_start
                    val = cm.dst_start + offset
                    break
        # print(seed, " -> ", val)
        location_nrs.append(val)

    print("Part1:", min(location_nrs))


# filename = "5/example"
filename = "5/input"
seeds, category_maps = parse(filename)
part1(seeds, category_maps)
