from collections import defaultdict, deque
from dataclasses import dataclass, field
import math
import re
import copy


PULSE_HI = "H"
PULSE_LO = "L"

TYPE_CON = "&"
TYPE_FLIP = "%"
TYPE_UNTYPED = "UNTYPED"


@dataclass
class Module:
    name: str
    type: str | None
    destinations: list["Module"] = field(default_factory=list)

    pulse_hi_cnt = 0
    pulse_lo_cnt = 0

    def __str__(self) -> str:
        s = ", ".join([d.name for d in self.destinations])
        return f"{self.type if self.type in [TYPE_CON, TYPE_FLIP] else ""}{self.name} -> {s}"


@dataclass
class FlipModule(Module):
    is_on: bool = False


@dataclass
class ConModule(Module):
    last_pulse_from: dict[str, str] = field(default_factory=dict)


@dataclass
class PulseInfo:
    pulse_from: Module | None
    pulse_to: Module
    pulse_type: str


def parse(filename: str) -> dict[str, Module]:
    # &jj -> hb, lz, rk, xv, vj, vh, lv

    d: dict[str, Module] = {}

    all_destinations = set()
    # create all modules
    with open(filename) as f:
        for line in f:
            line = line.strip()
            before, after = line.split(" -> ")
            type_ = before[0]

            destinations = after.split(", ")
            all_destinations |= set(destinations)

            m: Module | None = None

            if type_ == TYPE_FLIP:
                name = before[1:]
                m = FlipModule(name, type_)
            elif type_ == TYPE_CON:
                name = before[1:]
                m = ConModule(name, type_)
            else:
                name = before
                type_ = TYPE_UNTYPED
                m = Module(name, type_)

            assert name not in d, f"Duplicate module {name}"
            d[name] = m

    # special handing for output/last module
    while len(all_destinations) > 0:
        dest = all_destinations.pop()
        if dest not in d:
            d[dest] = Module(dest, TYPE_UNTYPED)

    # add destinations
    with open(filename) as f:
        for line in f:
            line = line.strip()
            before, after = line.split(" -> ")
            type_ = before[0]

            if type_ == TYPE_FLIP:
                name = before[1:]
            elif type_ == TYPE_CON:
                name = before[1:]
            else:
                name = before

            m = d[name]

            destinations = after.split(", ")

            for dest_name in destinations:
                dst = d[dest_name]
                m.destinations.append(dst)

                if dst.type == TYPE_CON:
                    assert isinstance(dst, ConModule)
                    dst.last_pulse_from[m.name] = PULSE_LO

            assert str(m) == line

    return d


def push_button(modules) -> tuple[int, int]:
    hi_cnt = 0
    lo_cnt = 0

    q: deque = deque()

    pi = PulseInfo(None, modules["broadcaster"], PULSE_LO)
    q.append(pi)

    while q:
        pi = q.popleft()

        # part 1
        if pi.pulse_type == PULSE_HI:
            hi_cnt += 1
        else:
            lo_cnt += 1

        # part 2
        if pi.pulse_type == PULSE_LO:
            pi.pulse_to.pulse_lo_cnt += 1
        else:
            pi.pulse_to.pulse_hi_cnt += 1

        # print(
        #     f"{pi.pulse_from.name if pi.pulse_from is not None else "button"} -{"low" if pi.pulse_type == PULSE_LO else "high"}-> {pi.pulse_to.name}"
        # )

        if pi.pulse_to.type == TYPE_CON:
            assert isinstance(pi.pulse_from, Module)
            assert isinstance(pi.pulse_to, ConModule)

            pi.pulse_to.last_pulse_from[pi.pulse_from.name] = pi.pulse_type

            is_all_hi = all(v == PULSE_HI for v in pi.pulse_to.last_pulse_from.values())
            if is_all_hi:
                next_pulse_type = PULSE_LO
            else:
                next_pulse_type = PULSE_HI

            for dest in pi.pulse_to.destinations:
                q.append(PulseInfo(pi.pulse_to, dest, next_pulse_type))

        elif pi.pulse_to.type == TYPE_FLIP:
            assert isinstance(pi.pulse_to, FlipModule)
            if pi.pulse_type == PULSE_LO:
                if pi.pulse_to.is_on:
                    next_pulse_type = PULSE_LO
                else:
                    next_pulse_type = PULSE_HI

                # flip
                pi.pulse_to.is_on = not pi.pulse_to.is_on

                for dest in pi.pulse_to.destinations:
                    q.append(PulseInfo(pi.pulse_to, dest, next_pulse_type))
        else:
            next_pulse_type = pi.pulse_type

            for dest in pi.pulse_to.destinations:
                q.append(PulseInfo(pi.pulse_to, dest, next_pulse_type))

    # print("")
    return hi_cnt, lo_cnt


def part1(modules):
    total_hi_cnt = 0
    total_lo_cnt = 0

    for i in range(1000):
        hi_cnt, lo_cnt = push_button(modules)
        total_hi_cnt += hi_cnt
        total_lo_cnt += lo_cnt

    print("Part 1:", total_hi_cnt * total_lo_cnt)


def part2(modules):
    i = 0
    while True:
        i += 1

        push_button(modules)
        m = modules["rx"]
        # if m.pulse_lo_cnt == 1 and m.pulse_hi_cnt == 0:
        print(m.pulse_lo_cnt, m.pulse_hi_cnt)
        if m.pulse_lo_cnt == 1:
            break

        m.pulse_lo_cnt = 0
        m.pulse_hi_cnt = 0

    # 999 too low
    print("Part 2:", i)


filename = "day20/example"
filename = "day20/input"

modules = parse(filename)
part1(copy.deepcopy(modules))
part2(copy.deepcopy(modules))
