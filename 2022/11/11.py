from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation_str: str
    test_divisible_by: int
    true_throw_to: int
    false_throw_to: int
    inspect_cnt: int = 0


monkeys = []


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
            print("Parsed:", m)

            pass
    return monkeys


def do_round(monkeys: list[Monkey]):
    for m in monkeys:
        m.inspect_cnt += len(m.items)
        while len(m.items) > 0:
            item = m.items.pop(0)
            item = operation(item, m.operation_str)
            item //= 3
            if item % m.test_divisible_by == 0:
                monkeys[m.true_throw_to].items.append(item)
            else:
                monkeys[m.false_throw_to].items.append(item)


# filename = "11/example"
filename = "11/input"
monkeys = parse(filename)

nr_of_rounds = 20
for i in range(nr_of_rounds):
    do_round(monkeys)

print(f"State after {nr_of_rounds} rounds:")
for m in monkeys:
    print(f"Monkey {m.id}: {m.items}")

for m in monkeys:
    print(f"Monkey {m.id} inspected items {m.inspect_cnt} times.")

inspects = [m.inspect_cnt for m in monkeys]
sorted_inspects = list(reversed(sorted(inspects)))
print("Monkey business:", sorted_inspects[0] * sorted_inspects[1])
