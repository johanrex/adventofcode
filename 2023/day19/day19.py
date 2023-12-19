from dataclasses import dataclass
import math
import re


re_workflow_s = r"(.+)\{(.+)\}"
re_workflow = re.compile(re_workflow_s)

re_parts_s = r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}"
re_parts = re.compile(re_parts_s)

re_cond_s = r"(.+)([<>])(.+):(.+)"
re_cond = re.compile(re_cond_s)


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int


@dataclass
class Rule:
    expression: str


@dataclass
class Workflow:
    name: str
    rules: list[Rule]


def parse(filename: str) -> tuple[dict[str, Workflow], list[Part]]:
    workflows: dict[str, Workflow] = {}
    parts: list[Part] = []

    parse_workflow = True
    with open(filename) as f:
        for line in f:
            line = line.strip()

            if line == "":
                parse_workflow = False
                continue

            if parse_workflow:
                match = re_workflow.match(line)
                assert match is not None

                name = match.group(1)
                rules_s = match.group(2)
                rules_l = rules_s.split(",")
                rules = [Rule(expression=ex) for ex in rules_l]

                workflows[name] = Workflow(name, rules)
            else:
                match = re_parts.match(line)

                assert match is not None

                x = int(match.group(1))
                m = int(match.group(2))
                a = int(match.group(3))
                s = int(match.group(4))

                parts.append(Part(x, m, a, s))

        return workflows, parts


def is_accepted(part: Part, workflows: dict[str, Workflow]) -> bool:
    # print(part, end=":")
    workflow = workflows["in"]
    while True:
        retval: bool | None = None
        # print(workflow.name, end=" -> ")
        for rule in workflow.rules:
            if rule.expression == "A":
                retval = True
                break
            elif rule.expression == "R":
                retval = False
                break
            elif (match := re_cond.match(rule.expression)) is not None:
                code = (
                    f"{part.__dict__[match.group(1)]} {match.group(2)} {match.group(3)}"
                )
                is_match = eval(code)
                if is_match:
                    action = match.group(4)

                    if action == "A":
                        retval = True
                        break
                    elif action == "R":
                        retval = False
                        break
                    else:
                        next_workflow = action
                        assert next_workflow in workflows
                        workflow = workflows[next_workflow]
                        break

            else:
                assert rule.expression in workflows

                workflow = workflows[rule.expression]
        if retval is not None:
            break

    # print("A" if retval else "R")
    return retval


def part1(workflows: dict[str, Workflow], parts: list[Part]):
    s = 0
    for part in parts:
        if is_accepted(part, workflows):
            s += part.x + part.m + part.a + part.s

    print("Part 1:", s)


def part2(workflows: dict[str, Workflow]):
    print("All workflows:")
    for w in workflows.values():
        print(w)
    print("")

    # build dependency graph, start from in
    # finns det workflows som inte används?
    # 1 <= value <= 4000
    # ringa in successivt hur många värden för varje rating.
    pass


filename = "day19/example"
# filename = "day19/input"

workflows, parts = parse(filename)
# part1(workflows, parts)
part2(workflows)
