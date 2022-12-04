def get_set(s):
    lst = s.split("-")
    i_from = int(lst[0])
    i_to = int(lst[1])
    assert i_from <= i_to
    set_of_numbers = set(range(i_from, i_to + 1))
    return set_of_numbers


nr_of_fully_contained = 0
nr_of_overlaps = 0
# with open("4/example") as f:
with open("4/input") as f:
    for line in f:
        line = line.strip()
        a, b = line.split(",")
        s1 = get_set(a)
        s2 = get_set(b)

        s_union = s1 | s2
        if s_union == s1 or s_union == s2:
            nr_of_fully_contained += 1

        if len(s_union) != (len(s1) + len(s2)):
            nr_of_overlaps += 1

print("Part1:", nr_of_fully_contained)
print("Part2:", nr_of_overlaps)

assert nr_of_fully_contained == 657
assert nr_of_overlaps == 938
