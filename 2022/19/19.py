from dataclasses import dataclass
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
        new_state.material_count = self.material_count.copy()
        new_state.robot_count = self.robot_count.copy()
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


# @cache
def can_produce_robot(state: State, bp: Blueprint, material_to_produce: Material) -> bool:
    materials_needed = bp.factory_costs[material_to_produce]

    for material in materials_needed:
        if material not in state.material_count or state.material_count[material] < materials_needed[material]:
            return False

    return True


def add_new_robot(state: State, bp: Blueprint, material_to_produce: Material) -> State:
    new_state = State()
    new_state.blueprint_id = bp.blueprint_id
    new_state.robot_count = state.robot_count.copy()
    new_state.robot_count[material_to_produce] = state.robot_count[material_to_produce] + 1

    new_state.material_count = state.material_count.copy()
    for material in bp.factory_costs[material_to_produce]:
        new_state.material_count[material] = state.material_count[material] - bp.factory_costs[material_to_produce][material]

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


# @cache
def get_next_possible_states(old_state: State, bp: Blueprint, current_time: int, stop_time: int) -> set[State]:
    possible_next_states: set[State] = set()

    if can_produce_robot(old_state, bp, Material.GEODE):
        new_state = add_new_robot(old_state, bp, Material.GEODE)
        possible_next_states.add(new_state)
    else:
        # TODO will produce more than theoretical maximum spend?
        time_left = stop_time - current_time

        if ((old_state.robot_count[Material.OBSIDIAN] * time_left) < (max_material_costs[Material.OBSIDIAN] * time_left)) and can_produce_robot(
            old_state, bp, Material.OBSIDIAN
        ):
            new_state = add_new_robot(old_state, bp, Material.OBSIDIAN)
            possible_next_states.add(new_state)

        if ((old_state.robot_count[Material.CLAY] * time_left) < (max_material_costs[Material.CLAY] * time_left)) and can_produce_robot(
            old_state, bp, Material.CLAY
        ):
            new_state = add_new_robot(old_state, bp, Material.CLAY)
            possible_next_states.add(new_state)

        if ((old_state.robot_count[Material.ORE] * time_left) < (max_material_costs[Material.ORE] * time_left)) and can_produce_robot(
            old_state, bp, Material.ORE
        ):
            new_state = add_new_robot(old_state, bp, Material.ORE)
            possible_next_states.add(new_state)

        # Add the "do nothing" state
        possible_next_states.add(old_state.copy())

    for new_state in possible_next_states:
        # Add one material for each robot that existed at old state.
        for material, robot_count in old_state.robot_count.items():
            new_state.material_count[material] += robot_count

    return possible_next_states


filename = "19/example"
# filename = "19/input"
bps = parse(filename)


sum_max_quality_levels = 0

for bp in bps:
    stop_time = 24

    bp_max_quality_level = 0

    prev_states: set[State] = set()

    max_material_costs = bp.get_max_material_cost()

    for current_time in range(stop_time):
        start_time = time.perf_counter()
        current_states: set[State] = set()

        if current_time == 0:
            current_states.add(get_initial_state(bp.blueprint_id))
        else:
            for prev_state in prev_states:
                current_states |= get_next_possible_states(prev_state, bp, current_time, stop_time)

        max_geodes = sorted([s.material_count[Material.GEODE] for s in current_states], reverse=True)[0]

        stop_time = time.perf_counter()

        if bp_max_quality_level < (bp.blueprint_id * max_geodes):
            bp_max_quality_level = bp.blueprint_id * max_geodes

        print(
            f"Minute {current_time+1} elapsed. Bp: {bp.blueprint_id}. States: {len(current_states)}. Max geodes: {max_geodes}. Max quality level: {bp_max_quality_level}. Speed: {len(current_states)/(stop_time-start_time):.2f} states/sec. Time: {(stop_time-start_time):.2f} sec."
        )

        prev_states = current_states
    sum_max_quality_levels += bp_max_quality_level

    pass

print("Part1:", sum_max_quality_levels)

# pip install pulp
# from pulp import LpMaximize, LpProblem, LpStatus, LpVariable
