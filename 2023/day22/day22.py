from collections import deque
from dataclasses import dataclass
import math
import re
import copy
import sys


Coord = tuple[int, int, int]
Coords = list[tuple[Coord, Coord]]


def parse(filename: str) -> Coords:
    coords: Coords = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            a, b = line.split("~")
            a_ints = tuple(map(int, a.split(",")))
            b_ints = tuple(map(int, b.split(",")))
            a_c = (a_ints[0], a_ints[1], a_ints[2])
            b_c = (b_ints[0], b_ints[1], b_ints[2])
            coords.append((a_c, b_c))

    return coords


def verify_assumption1(coords: Coords):
    # first coordinate has lower or equal z coordinate
    for f, t in coords:
        _, _, fz = f
        _, _, tz = t
        assert fz <= tz


def verify_assumption2(coords: Coords):
    # verify that everything is between [0,1000)
    for f, t in coords:
        for i in range(3):
            assert 0 <= f[i] < 1000
            assert 0 <= t[i] < 1000


def sort_by_from_z_func(tpl: tuple[Coord, Coord]) -> int:
    key = tpl[0][2] * 1000 + tpl[1][2]
    return key


def sort_by_to_z_func(tpl: tuple[Coord, Coord]) -> int:
    key = tpl[1][2] * 1000 + tpl[0][2]
    return key


def has_overlap_x_y(f1: Coord, t1: Coord, f2: Coord, t2: Coord) -> bool:
    fx1, fy1, _ = f1
    tx1, ty1, _ = t1
    fx2, fy2, _ = f2
    tx2, ty2, _ = t2

    assert fx1 <= tx1
    assert fy1 <= ty1
    assert fx2 <= tx2
    assert fy2 <= ty2

    overlap_x = f1[0] <= t2[0] and t1[0] >= f2[0]
    overlap_y = f1[1] <= t2[1] and t1[1] >= f2[1]

    return overlap_x and overlap_y


def has_overlap_x_y_z(f1: Coord, t1: Coord, f2: Coord, t2: Coord) -> bool:
    overlap_x = f1[0] <= t2[0] and t1[0] >= f2[0]
    overlap_y = f1[1] <= t2[1] and t1[1] >= f2[1]
    overlap_z = f1[2] <= t2[2] and t1[2] >= f2[2]

    return overlap_x and overlap_y and overlap_z


def assert_distinct(coords: Coords):
    for i in range(len(coords)):
        f1, t1 = coords[i]
        for j in range(i + 1, len(coords)):
            f2, t2 = coords[j]
            assert not has_overlap_x_y_z(f1, t1, f2, t2)


def assert_all_is_at_rest(coords: Coords):
    for i in range(len(coords)):
        f1, t1 = coords[i]
        for j in range(len(coords)):
            if i == j:
                continue

            f2, t2 = coords[j]
            pass


def fall(coords: Coords) -> dict[tuple[Coord, Coord], tuple[Coord, Coord]]:
    falling = deque(sorted(coords, key=sort_by_from_z_func))

    lookup = {}
    at_rest: Coords = []

    while len(falling) > 0:
        f, t = falling.popleft()

        new_z = 1

        if len(at_rest) == 0:
            new_z = 1
        else:
            at_rest_overlap_xy = sorted(
                [
                    resting
                    for resting in at_rest
                    if has_overlap_x_y(f, t, resting[0], resting[1])
                ],
                key=sort_by_to_z_func,
                reverse=True,
            )
            if len(at_rest_overlap_xy) > 0:
                highest = at_rest_overlap_xy[0]
                new_z = highest[1][2] + 1

        height = t[2] - f[2]

        at_rest_f = (f[0], f[1], new_z)
        at_rest_t = (t[0], t[1], new_z + height)

        # print(f"Brick {f}{t} falls to {at_rest_f}{at_rest_t}")

        at_rest.append((at_rest_f, at_rest_t))
        # dbg
        # assert_distinct(at_rest)

        lookup[(at_rest_f, at_rest_t)] = (f, t)

    return lookup


def is_resting_on(bottom_f: Coord, bottom_t: Coord, top_f: Coord, top_t: Coord) -> bool:
    assert not (bottom_f == top_f and bottom_t == top_t)

    # check if top is directly above bottom
    if top_f[2] != bottom_t[2] + 1:
        return False

    return has_overlap_x_y(bottom_f, bottom_t, top_f, top_t)


def is_supporting(
    bottom_f: Coord, bottom_t: Coord, at_rest: Coords
) -> list[tuple[Coord, Coord]]:
    tops = []
    for top_f, top_t in at_rest:
        if bottom_f == top_f and bottom_t == top_t:
            continue
        if is_resting_on(bottom_f, bottom_t, top_f, top_t):
            tops.append((top_f, top_t))
    return tops


def is_supported_by(
    top_f: Coord, top_t: Coord, at_rest: Coords
) -> list[tuple[Coord, Coord]]:
    bottoms = []

    for bottom_f, bottom_t in at_rest:
        if bottom_f == top_f and bottom_t == top_t:
            continue

        if is_resting_on(bottom_f, bottom_t, top_f, top_t):
            bottoms.append((bottom_f, bottom_t))

    return bottoms


def part1(lookup: dict[tuple[Coord, Coord], tuple[Coord, Coord]]):
    at_rest = list(lookup.keys())
    # assert_distinct(at_rest)

    # print("At rest:")
    # for brick in at_rest:
    #     print(brick)
    # print("")

    s = 0
    for f, t in at_rest:
        tops = is_supporting(f, t, at_rest)
        if len(tops) == 0:
            # print(f"{lookup[(f,t)]} can be disintegrated. It doesn't support anything.")
            s += 1
        else:
            is_lone_supporter_of_at_least_one = False
            for top_f, top_t in tops:
                bottoms = is_supported_by(top_f, top_t, at_rest)
                if len(bottoms) == 1:
                    is_lone_supporter_of_at_least_one = True

            tops_strs = [f"{lookup[top]}" for top in tops]
            if is_lone_supporter_of_at_least_one:
                pass
                # print(
                #     f"{lookup[(f,t)]} cannot be disintegrated safely. If it were disintegrated, bricks {' and '.join(tops_strs)} would fall."
                # )
            else:
                # print(
                #     f"{lookup[(f,t)]} can be disintegrated. The bricks above it {'and'.join(tops_strs)} would still be supported."
                # )
                s += 1

    print("Part 1:", s)


def part2(lookup: dict[tuple[Coord, Coord], tuple[Coord, Coord]]):
    at_rest = list(lookup.keys())

    # create graph/tree

    print("Part 2:", -1)


filename = "day22/example"
filename = "day22/input"

coords = parse(filename)

verify_assumption1(coords)
verify_assumption2(coords)
# assert_distinct(coords)
lookup = fall(coords)
part1(lookup)
part2(lookup)
