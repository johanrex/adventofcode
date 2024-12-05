from collections import defaultdict


def parse_input(filename: str):
    with open(filename) as f:
        text = f.read()

    rules_section, updates_section = text.strip().split("\n\n")

    rules = defaultdict(set)
    # Parse rules into pairs
    for line in rules_section.split("\n"):
        before, after = map(int, line.split("|"))
        rules[before].add(after)

    # Parse orders into lists of numbers
    updates = []
    for line in updates_section.split("\n"):
        update = [int(x) for x in line.split(",")]
        assert len(update) % 2 == 1
        updates.append(update)

    return rules, updates


def is_valid_order(update, rule_graph):
    # are all rules ok?
    seen = set()
    for num in update:
        for prev in seen:
            if num in rule_graph[prev]:
                continue
            else:
                return False
        seen.add(num)
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

    s = sum_of_middle_elements(updates_not_in_order)
    assert s == 5479
    print("Part 2:", s)


# filename = "day5/example"
filename = "day5/input"

rules, updates = parse_input(filename)

updates_in_order = []
updates_not_in_order = []
for update in updates:
    if is_valid_order(update, rules):
        updates_in_order.append(update)
    else:
        updates_not_in_order.append(update)
part1(updates_in_order)
print("")
part2(rules, updates_not_in_order)
