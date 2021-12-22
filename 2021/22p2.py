from __future__ import annotations 
from dataclasses import dataclass
from typing import List
import re

#example 'on x=-10..44,y=-47..3,z=-30..20'
p = re.compile('(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')

@dataclass
class Cube:
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @staticmethod
    def get_intersect(first: Cube, second: Cube):
        if (
            ((first.x[0] <= second.x[0] <= first.x[1]) or (second.x[0] <= first.x[0] <= second.x[1])) and 
            ((first.y[0] <= second.y[0] <= first.y[1]) or (second.y[0] <= first.y[0] <= second.y[1])) and 
            ((first.z[0] <= second.z[0] <= first.z[1]) or (second.z[0] <= first.z[0] <= second.z[1]))
        ):
            overlap_start_x = max(first.x[0], second.x[0])
            overlap_end_x = min(first.x[1], second.x[1])

            overlap_start_y = max(first.y[0], second.y[0])
            overlap_end_y = min(first.y[1], second.y[1])

            overlap_start_z = max(first.z[0], second.z[0])
            overlap_end_z = min(first.z[1], second.z[1])

            intersecting_cube = Cube(
                x=(overlap_start_x, overlap_end_x),
                y=(overlap_start_y, overlap_end_y),
                z=(overlap_start_z, overlap_end_z))

            return intersecting_cube
        else:
            return None


@dataclass
class Instruction:
    operation: str
    cube: Cube

    def __str__(self) -> str:
        return f'{self.operation} x={self.cube.x[0]}..{self.cube.x[1]},y={self.cube.y[0]}..{self.cube.y[1]},z={self.cube.z[0]}..{self.cube.z[1]}'


def parse_input(filename: str) -> List[Instruction]:
    instructions = []
    with open(filename) as f:
        for line in f:
            line = line.strip()

            m = p.match(line)

            cube = Cube(x=(int(m[2]), int(m[3])), y=(int(m[4]), int(m[5])), z=(int(m[6]), int(m[7])))

            assert (
                cube.x[0] < cube.x[1] and 
                cube.y[0] < cube.y[1] and 
                cube.z[0] < cube.z[1])

            instructions.append(Instruction(operation=1 if m[1] == 'on' else 0, cube=cube))

    return instructions


def do_instruction(inst):
    #check if new cube intersects with any existing cube. 

    for cube in cubes:
        if Cube.get_intersect(inst.cube, cube):
            print('yes')

    cubes.append(inst.cube)

c1 = Cube(x=(0,10), y=(0,10), z=(0,10))
c2 = Cube(x=(0,5), y=(0,5), z=(0,5))

intersect = Cube.get_intersect(c1, c2)




#filename = '2021/22_input_example.txt'
filename = '2021/22_input.txt'
instructions = parse_input(filename)

print('Nr of instructions:', len(instructions))

#Rule: No cubes in the list should intersect anywhere. 
cubes = []

for i, inst in enumerate(instructions):
    print('Executing instruction:', i+1)

    do_instruction(inst)



"""
Del 2

lista med kuber

on: dela upp i mindre cubes så att man bara lägger till där det inte redan ligger något. 
off. ta bort och splitta upp befintliga kuber i mindre kuber. 


"""
