from dataclasses import dataclass, field
from enum import IntEnum
from functools import cache
import re
from typing import Self
import json
import time

pat = re.compile(
    r"Blueprint (?P<blueprint_id>\d+): Each ore robot costs (?P<ore_robot_cost_ore>\d+) ore. Each clay robot costs (?P<clay_robot_cost_ore>\d+) ore. Each obsidian robot costs (?P<obsidian_robot_cost_ore>\d+) ore and (?P<obsidian_robot_cost_clay>\d+) clay. Each geode robot costs (?P<geode_robot_cost_ore>\d+) ore and (?P<geode_robot_cost_obsidian>\d+) obsidian."
)


class Material(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


@dataclass
class Blueprint:
    blueprint_id: int
    factory_costs: dict[Material, dict[Material, int]]

    def get_max_material_cost(self) -> dict[Material, int]:
        max_material_cost = {m: 0 for m in Material}

        for _, material_costs in self.factory_costs.items():
            for material, cost in material_costs.items():
                if max_material_cost[material] < cost:
                    max_material_cost[material] = cost

        return max_material_cost

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, o: object) -> bool:
        return self.__repr__() == o.__repr__()


class State:
    def __init__(self) -> None:
        self.blueprint_id: int
        self.material_count: dict[Material, int]
        self.robot_count: dict[Material, int]

    def copy(self) -> Self:
        new_state = State()
        new_state.blueprint_id = self.blueprint_id
        new_state.material_count = {k: v for k, v in self.material_count.items()}
        new_state.robot_count = {k: v for k, v in self.robot_count.items()}
        return new_state

    def __eq__(self, o: object) -> bool:
        return self.__repr__() == o.__repr__()

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)

    def __str__(self) -> str:
        materials = ""
        robots = ""
        for material in Material:
            materials += f" {material.name}:{self.material_count[material]}"
            robots += f" {material.name}:{self.robot_count[material]}"

        msg = f"Bp: {self.blueprint_id}. Materials:{materials}. Robots:{robots}"

        return msg


# TODO don't need tree.
@dataclass
class TreeNode:
    value: State
    parent: Self | None
    children: list[Self] = field(default_factory=list)


@cache
def can_buy_robot(state: State, bp: Blueprint, material_to_produce: Material) -> bool:
    materials_needed = bp.factory_costs[material_to_produce]

    for material_needed, cost in materials_needed.items():
        if state.material_count[material_needed] < cost:
            return False

    return True


def buy_new_robot(state: State, bp: Blueprint, material_to_produce: Material) -> State:
    new_state = state.copy()
    new_state.robot_count[material_to_produce] = state.robot_count[material_to_produce] + 1

    materials_needed = bp.factory_costs[material_to_produce]
    for material, cost in materials_needed.items():
        new_state.material_count[material] = state.material_count[material] - cost

    return new_state


def get_initial_state(bp_id: int) -> State:
    state = State()
    state.blueprint_id = bp_id
    state.material_count = dict()
    state.robot_count = dict()

    for material in Material:
        state.material_count[material] = 0
        state.robot_count[material] = 0

    state.robot_count[Material.ORE] = 1
    # state.material_count[Material.ORE] = 1
    return state


def parse(filename) -> list[Blueprint]:
    bps = []
    with open(filename) as f:
        for line in f:
            m = re.match(pat, line.strip())
            if m is None:
                raise Exception("oops")

            bp = Blueprint(
                blueprint_id=int(m.group("blueprint_id")),
                factory_costs={
                    Material.ORE: {Material.ORE: int(m.group("ore_robot_cost_ore"))},
                    Material.CLAY: {Material.ORE: int(m.group("clay_robot_cost_ore"))},
                    Material.OBSIDIAN: {
                        Material.ORE: int(m.group("obsidian_robot_cost_ore")),
                        Material.CLAY: int(m.group("obsidian_robot_cost_clay")),
                    },
                    Material.GEODE: {
                        Material.ORE: int(m.group("geode_robot_cost_ore")),
                        Material.OBSIDIAN: int(m.group("geode_robot_cost_obsidian")),
                    },
                },
            )

            bps.append(bp)

    return bps


def print_bp(bp: Blueprint):
    msg = f"Blueprint {bp.blueprint_id}:"

    for material, cost in bp.factory_costs.items():
        msg += f" Each {material.name.lower()} robot costs"
        for cost_material, cost_count in cost.items():
            msg += f" {cost_count} {cost_material.name.lower()}"
        msg += "."

    print(msg)


def get_do_nothing_state(old_state: State, bp: Blueprint):
    new_state = old_state.copy()

    return new_state


# @cache
def get_next_possible_states(old_state: State, bp: Blueprint, current_time: int, stop_time: int) -> set[State]:
    next_states: set[State] = set()
    time_left = stop_time - current_time

    if time_left <= 1:
        # Add the "do nothing" state
        next_states.add(old_state.copy())
    else:
        if can_buy_robot(old_state, bp, Material.GEODE):
            next_states.add(buy_new_robot(old_state, bp, Material.GEODE))
        else:
            if can_buy_robot(old_state, bp, Material.OBSIDIAN):
                next_states.add(buy_new_robot(old_state, bp, Material.OBSIDIAN))

            if can_buy_robot(old_state, bp, Material.CLAY):
                next_states.add(buy_new_robot(old_state, bp, Material.CLAY))

            if ((old_state.robot_count[Material.ORE] * time_left) < (max_material_costs[Material.ORE] * time_left)) and can_buy_robot(
                old_state, bp, Material.ORE
            ):
                next_states.add(buy_new_robot(old_state, bp, Material.ORE))

            if old_state.material_count[Material.ORE] < max_material_costs[Material.ORE]:
                # Add the "do nothing" state
                next_states.add(old_state.copy())

    # collect output from working robots
    for next_state in next_states:
        for material, count in old_state.robot_count.items():
            next_state.material_count[material] += count

    return next_states


def dfs(bp: Blueprint, node: TreeNode, stop_time: int, current_time: int = 0) -> int:
    old_state = node.value

    if current_time == stop_time:
        return old_state.material_count[Material.GEODE]

    next_states = get_next_possible_states(old_state, bp, current_time, stop_time)

    for next_state in next_states:
        node.children.append(TreeNode(value=next_state, parent=node))

    max_geodes = 0
    for child in node.children:
        child_geodes = dfs(bp, child, stop_time, current_time + 1)
        max_geodes = max(max_geodes, child_geodes)

    return max_geodes


# filename = "19/example"
filename = "19/input"
bps = parse(filename)

sum_max_quality_levels = 0
stop_time: int = 24

for bp in bps:
    print(f"Bp: {bp.blueprint_id}.")
    max_material_costs = bp.get_max_material_cost()
    bp_max_quality_level = 0
    state = get_initial_state(bp.blueprint_id)
    root = TreeNode(value=state, parent=None)
    max_geodes = dfs(bp, root, stop_time)
    print(f"Max geodes found: {max_geodes}.")
    sum_max_quality_levels += max_geodes * bp.blueprint_id


# t1 = time.perf_counter()
# t2 = time.perf_counter()

# msg = ""
# msg += f"Bp: {bp.blueprint_id}."
# msg += f" Minute {str(current_time+1).ljust(2)}."
# msg += f" States: {str(len(current_states)).ljust(7)}. Max geodes: {max_geodes}. Max quality level: {bp_max_quality_level}."
# msg += f" Speed: {len(current_states)/(t2-t1):.2f} states/sec. Time: {(t2-t1):.2f} sec."
# print(msg)

# 1366 too low
# 1395 troligen rätt svar.
print("Part1:", sum_max_quality_levels)
