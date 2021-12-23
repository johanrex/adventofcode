from __future__ import annotations 
from dataclasses import dataclass
from typing import List
import re

#example 'on x=-10..44,y=-47..3,z=-30..20'
p = re.compile('(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __eq__(self, other: Point) -> bool:
        return (
            self.x == other.x and
            self.y == other.y and
            self.z == other.z)

@dataclass
class Cube:
    start: Point
    end: Point

    def __eq__(self, other: Cube) -> bool:
        return (
            self.start == other.start and
            self.end == other.end)


    def volume(self):
        return (self.end.x - self.start.x) * (self.end.y - self.start.y) * (self.end.z - self.start.z)


    @staticmethod
    def intersect(first: Cube, second: Cube):
        if (
            ((first.start.x <= second.start.x <= first.end.x) or (second.start.x <= first.start.x <= second.end.x)) and 
            ((first.start.y <= second.start.y <= first.end.y) or (second.start.y <= first.start.y <= second.end.y)) and 
            ((first.start.z <= second.start.z <= first.end.z) or (second.start.z <= first.start.z <= second.end.z))
        ):
            overlap_start_x = max(first.start.x, second.start.x)
            overlap_end_x = min(first.end.x, second.end.x)

            overlap_start_y = max(first.start.y, second.start.y)
            overlap_end_y = min(first.end.y, second.end.y)

            overlap_start_z = max(first.start.z, second.start.z)
            overlap_end_z = min(first.end.z, second.end.z)

            intersecting_cube = Cube(
                start=Point(x=overlap_start_x, y=overlap_start_y, z=overlap_start_z),
                end=Point(x=overlap_end_x, y=overlap_end_y, z=overlap_end_z))
            return intersecting_cube
        else:
            return None


@dataclass
class Instruction:
    operation: str
    cube: Cube

    def __str__(self) -> str:
        return f'{self.operation} x={self.cube.start.x}..{self.cube.end.x},y={self.cube.start.y}..{self.cube.end.y},z={self.cube.start.z}..{self.cube.end.z}'


def parse_input(filename: str) -> List[Instruction]:
    instructions = []

    with open(filename) as f:
        for line in f:
            line = line.strip()

            m = p.match(line)

            cube = Cube(
                start=Point(x=int(m[2]), y=int(m[4]), z=int(m[6])),
                end=Point(x=int(m[3]), y=int(m[5]), z=int(m[7])))

            assert (
                cube.start.x < cube.end.x and 
                cube.start.y < cube.end.y and 
                cube.start.z < cube.end.z)

            instruction = Instruction(operation=m[1], cube=cube)

            assert line == str(instruction)

            instructions.append(instruction)

    return instructions

def tests():

    c1 = Cube(start=Point(0,0,0), end=Point(10,10,10))
    c2 = Cube(start=Point(10,10,10), end=Point(12,12,12))

    intersect = Cube.intersect(c1, c2)


def get_x_low_high(instructions: Instruction):
    lo = instructions[0].cube.start.x
    hi = instructions[0].cube.end.x

    for i in range(1, len(instructions)):
        inst = instructions[i]
        hi = inst.cube.end.x if inst.cube.end.x > hi else hi
        lo = inst.cube.start.x if inst.cube.start.x < lo else lo
            
    return lo, hi


def get_y_low_high(instructions: Instruction):
    lo = instructions[0].cube.start.y
    hi = instructions[0].cube.end.y

    for i in range(1, len(instructions)):
        inst = instructions[i]
        hi = inst.cube.end.y if inst.cube.end.y > hi else hi
        lo = inst.cube.start.y if inst.cube.start.y < lo else lo
            
    return lo, hi


def get_z_low_high(instructions: Instruction):
    lo = instructions[0].cube.start.z
    hi = instructions[0].cube.end.z

    for i in range(1, len(instructions)):
        inst = instructions[i]
        hi = inst.cube.end.z if inst.cube.end.z > hi else hi
        lo = inst.cube.start.z if inst.cube.start.z < lo else lo
            
    return lo, hi


def count(instructions):

    x_range = get_x_low_high(instructions)

    sum = 0

    for x in range(x_range[0], x_range[1]+1):
        x_inputs = [input for input in instructions if input.cube.start.x <= x <= input.cube.end.x]

        print(f'{((x-x_range[0]) / (x_range[1] - x_range[0]) * 100):.2f}%')

        if len(x_inputs) > 0:

            y_range = get_y_low_high(x_inputs)

            for y in range(y_range[0], y_range[1]+1):
                xy_inputs = [input for input in x_inputs if input.cube.start.y <= y <= input.cube.end.y]

                if len(xy_inputs) > 0:

                    z_range = get_z_low_high(xy_inputs)                        

                    for z in range(z_range[0], z_range[1]+1):
                        xyz_inputs = [input for input in xy_inputs if input.cube.start.z <= z <= input.cube.end.z]

                        if len(xyz_inputs) > 0:
                            #order is preserved in list comprehensions so we should just be able to get the last one. 
                            last_relevant_input = next(reversed(xyz_inputs))

                            if last_relevant_input.operation == 'on':

                                sum += 1
    return sum


def part1_instructions(instructions):
    part1_instructions = []

    for inst in instructions:
        if (
            (inst.cube.start.x in range(-50, 51) and inst.cube.end.x in range(-50, 51)) and 
            (inst.cube.start.y in range(-50, 51) and inst.cube.end.y in range(-50, 51)) and 
            (inst.cube.start.z in range(-50, 51) and inst.cube.end.z in range(-50, 51))
            ):
            part1_instructions.append(inst)
    
    return part1_instructions


#filename = '2021/22_input_example.txt'
filename = '2021/22_input.txt'
instructions = parse_input(filename)

print('Part 1:', count(part1_instructions(instructions))) #611176

print('Part 2:', count(instructions))

