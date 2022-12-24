import re

re.match
# filename = "18/example"
filename = "19/input"

# line = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 2 ore and 16 clay. Each geode robot costs 4 ore and 16 obsidian."
pat = re.compile(
    r"Blueprint (?P<blueprint_nr>\d+): Each ore robot costs (?P<ore_robot_cost_ore>\d+) ore. Each clay robot costs (?P<clay_robot_cost_ore>\d+) ore. Each obsidian robot costs (?P<obsidian_robot_cost_ore>\d+) ore and (?P<obsidian_robot_cost_clay>\d+) clay. Each geode robot costs (?P<geode_robot_cost_ore>\d+) ore and (?P<geode_robot_cost_obsidian>\d+) obsidian."
)


with open(filename) as f:
    for line in f:
        m = re.match(pat, line.strip())
        if m is None:
            raise Exception("oops")

        blueprint_nr = m.group("blueprint_nr")
        ore_robot_cost_ore = m.group("ore_robot_cost_ore")
        clay_robot_cost_ore = m.group("clay_robot_cost_ore")
        obsidian_robot_cost_ore = m.group("obsidian_robot_cost_ore")
        obsidian_robot_cost_clay = m.group("obsidian_robot_cost_clay")
        geode_robot_cost_ore = m.group("geode_robot_cost_ore")
        geode_robot_cost_obsidian = m.group("geode_robot_cost_obsidian")

        print(blueprint_nr)

"""
maximize geodes in 24 minutes.

ore -> ore_robot
ore -> clay_robot
ore + clay  -> obsidian_robot
ore + obsidian -> geode_robot
"""

# pip install pulp
# from pulp import LpMaximize, LpProblem, LpStatus, LpVariable
