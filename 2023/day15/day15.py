from dataclasses import dataclass, field
import math
import re

pat = r"([a-z]+)([-=])(\d*)"
r = re.compile(pat)


@dataclass
class Lens:
    label: str
    focal_length: int


@dataclass
class Box:
    lenses: list[Lens] = field(default_factory=list)


def parse(filename):
    with open(filename) as f:
        s = ""
        for line in f:
            s += line.strip()

        init_seq = s.split(",")
    return init_seq


def hash_seq(seq):
    h = 0
    for c in seq:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def part1(init_seq):
    s = 0
    for inst in init_seq:
        s += hash_seq(inst)

    print("Part 1:", s)


def part2(init_seq):
    boxes = []
    for _ in range(256):
        boxes.append(Box())

    for step in init_seq:
        m = r.match(step)
        lbl = m.group(1)

        box_idx = hash_seq(lbl)
        box = boxes[box_idx]

        op = m.group(2)
        if op == "-":
            for lens in box.lenses:
                if lens.label == lbl:
                    box.lenses.remove(lens)
                    break

        if op == "=":
            focal_length = int(m.group(3))
            found = False
            for lens in box.lenses:
                if lens.label == lbl:
                    lens.focal_length = focal_length
                    found = True
                    break

            if not found:
                box.lenses.append(Lens(lbl, focal_length))

    focusing_power = 0

    for box_nr, box in enumerate(boxes):
        for slot_idx, lens in enumerate(box.lenses):
            slot_nr = slot_idx + 1
            lens_focusing_power = (box_nr + 1) * slot_nr * lens.focal_length
            focusing_power += lens_focusing_power

    print("Part 2:", focusing_power)


filename = "day15/example"
filename = "day15/input"

init_seq = parse(filename)
part1(init_seq)
part2(init_seq)
