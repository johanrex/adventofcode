from collections import defaultdict, deque
from dataclasses import dataclass, field
import math
import re


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


def part1(modules):
    lo_pulse_cnt = 0
    hi_pulse_cnt = 0

    q = deque()

    # from to type
    pi = PulseInfo(None, modules["broadcaster"], PULSE_LO)
    q.append(pi)

    while q:
        pi = q.popleft()

        print(
            f"{pi.pulse_from.name if pi.pulse_from is not None else "button"} -{"low" if pi.pulse_type == PULSE_LO else "high"}-> {pi.pulse_to.name}"
        )

        if pi.pulse_to.type == TYPE_CON:
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

    print("Part 1:", -1)


filename = "day20/example"
# filename = "day20/input"

modules = parse(filename)
part1(modules)
