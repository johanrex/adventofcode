from dataclasses import dataclass


magic_nr = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation_str: str
    test_divisible_by: int
    true_throw_to: int
    false_throw_to: int
    inspect_cnt: int = 0


"""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
"""


def operation(old, op_str):
    new = eval(op_str)
    return new


def parse(filename):
    monkeys = []
    with open(filename) as f:
        while line := f.readline():
            assert line.startswith("Monkey ")
            monkey_id = int(line[7])
            items = list(map(int, f.readline().strip()[16:].split(",")))
            line = f.readline().strip()
            operation_str = line[17:]
            line = f.readline().strip()
            test_divisible_by = int(line[19:])
            line = f.readline().strip()
            true_throw_to = int(line[25])
            line = f.readline().strip()
            false_throw_to = int(line[26])
            assert "" == f.readline().strip()

            m = Monkey(
                id=monkey_id,
                items=items,
                operation_str=operation_str,
                test_divisible_by=test_divisible_by,
                true_throw_to=true_throw_to,
                false_throw_to=false_throw_to,
            )

            monkeys.append(m)
    return monkeys


def do_round(monkeys: list[Monkey], divide: bool):
    for m in monkeys:
        m.inspect_cnt += len(m.items)
        while len(m.items) > 0:
            item = m.items.pop(0)
            item = operation(item, m.operation_str)

            if divide:
                item //= 3
            elif item > magic_nr:
                item %= magic_nr

            if item % m.test_divisible_by == 0:
                monkeys[m.true_throw_to].items.append(item)
            else:
                monkeys[m.false_throw_to].items.append(item)


def print_stats(monkeys, nr_of_rounds):
    print(f"State after {nr_of_rounds} rounds:")
    for m in monkeys:
        print(f"Monkey {m.id}: {m.items}")

    print("")

    for m in monkeys:
        print(f"Monkey {m.id} inspected items {m.inspect_cnt} times.")


def get_monkey_business(filename: str, divide: bool, nr_of_rounds: int):
    monkeys = parse(filename)

    for _ in range(nr_of_rounds):
        do_round(monkeys, divide)

    # print_stats(monkeys, nr_of_rounds)

    inspects = [m.inspect_cnt for m in monkeys]
    sorted_inspects = list(reversed(sorted(inspects)))
    monkey_business = sorted_inspects[0] * sorted_inspects[1]
    return monkey_business


# filename = "11/example"
filename = "11/input"

monkey_business = get_monkey_business(filename, divide=True, nr_of_rounds=20)
assert 78960 == monkey_business
print("Part1:", monkey_business)

monkey_business = get_monkey_business(filename, divide=False, nr_of_rounds=10000)
assert 14561971968 == monkey_business
print("Part2:", monkey_business)
