"""
You make a map (your puzzle input) of the open squares (.) and trees (#) you can see.

Starting at the top-left corner of your map and following a slope of right 3 and down 1, 
how many trees would you encounter?
"""

with open("day3_input.txt") as f:
    lines = f.readlines()

# strip newlines
lines = [line.strip() for line in lines]

lines_count = len(lines)
rows_count = len(lines[0])


def count_trees(right_count, down_count):
    vpos = 0
    hpos = 0
    offset = 0
    trees = 0
    while vpos < len(lines):
        if lines[vpos][offset] == "#":
            trees += 1

        vpos += down_count
        hpos += right_count
        offset = hpos % rows_count

    return trees


def part1():
    print("Part 1:", count_trees(3, 1))


def part2():

    prod = count_trees(1, 1) * count_trees(3, 1) * count_trees(5, 1) * count_trees(7, 1) * count_trees(1, 2)

    print("Part 2:", prod)


part1()
part2()
