from collections import defaultdict

parent_to_children = defaultdict(list)


def parse(filename: str):
    with open(filename) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    for line in lines:
        parent_color, children = line.split(" contain ")
        parent_color = parent_color.removesuffix("bags").strip()

        children = children.rstrip(".")
        children = children.split(", ")
        children = [child.strip() for child in children]

        child_list = []

        if len(children) == 1 and children[0] == "no other bags":
            continue
        else:
            for child in children:
                idx = child.find(" ")

                child_count = int(child[:idx])

                child_color = child[idx + 1 :]
                child_color = child_color.removesuffix(" bags").removesuffix(" bag").strip()

                child_list.append((child_count, child_color))

        parent_to_children[parent_color] = child_list

    return parent_to_children


def dfs_contains_target(parent_to_children: dict, current_color: str, target_color: str) -> bool:
    if current_color == target_color:
        return True

    for child_tpl in parent_to_children[current_color]:
        _, child_color = child_tpl
        if dfs_contains_target(parent_to_children, child_color, target_color):
            return True

    return False


def dfs_count_bags(parent_to_children: dict, current_color: str) -> int:
    cnt = 1
    for child_tpl in parent_to_children[current_color]:
        child_count, child_color = child_tpl
        cnt += child_count * dfs_count_bags(parent_to_children, child_color)
    return cnt


filename = "day7/input"

parent_to_children = parse(filename)

target_color = "shiny gold"

cnt = 0
for color in list(parent_to_children.keys()):
    if color == target_color:
        continue
    if dfs_contains_target(parent_to_children, color, target_color):
        cnt += 1


print("Part 1:", str(cnt))

cnt_part2 = dfs_count_bags(parent_to_children, target_color) - 1
print("Part 2:", str(cnt_part2))
