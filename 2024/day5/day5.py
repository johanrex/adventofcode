from collections import defaultdict


def parse_input(filename: str):
    rules = defaultdict(set)
    updates = []

    first_section = True
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if line == "":
            first_section = False
            continue

        if first_section:
            # we're parsing rules
            before, after = map(int, line.split("|"))
            rules[before].add(after)
        else:
            # we're parsing updates
            update = [int(x) for x in line.split(",")]
            updates.append(update)
            assert len(update) % 2 == 1

    return rules, updates


def is_valid_order(update, rules):
    # are all rules satisfied?
    prevs = set()
    for num in update:
        for prev in prevs:
            if num in rules[prev]:
                continue
            else:
                return False
        prevs.add(num)
    return True


def sum_of_middle_elements(updates):
    s = 0
    for update in updates:
        middle = update[len(update) // 2]
        s += middle
    return s


def part1(updates_in_order):
    s = sum_of_middle_elements(updates_in_order)
    assert s == 5991
    print("Part 1:", s)


def part2(rules, updates_not_in_order):
    for update in updates_not_in_order:
        # print("Considering update:")
        # print(update)

        maybe_things_to_flip = True
        while maybe_things_to_flip:
            maybe_things_to_flip = False
            for i in range(len(update) - 1):
                before = update[i]
                after = update[i + 1]

                if after in rules[before]:
                    # all is well
                    continue
                else:
                    # flip
                    update[i] = after
                    update[i + 1] = before
                    maybe_things_to_flip = True

                    # print("Flipped:", before, after, "->", after, before)
                    # print("Update is now:")
                    # print(update)
                    break
            # print("Final update is now:")
            # print(update)

        # print("")

    # at this point, all updates are in order
    s = sum_of_middle_elements(updates_not_in_order)
    assert s == 5479
    print("Part 2:", s)


# filename = "day5/example"
filename = "day5/input"

rules, updates = parse_input(filename)

updates_in_order = [u for u in updates if is_valid_order(u, rules)]
updates_not_in_order = [u for u in updates if not is_valid_order(u, rules)]

part1(updates_in_order)
part2(rules, updates_not_in_order)
