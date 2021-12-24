from __future__ import annotations 
from dataclasses import dataclass
from typing import List
import re

from timeit import default_timer as timer
t1 = timer()

#example: 'on x=-10..44,y=-47..3,z=-30..20'
p = re.compile('(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')


@dataclass
class Instruction:
    operation: str
    xs: list[int]
    ys: list[int]
    zs: list[int]

    def __str__(self) -> str:
        return f'{self.operation} x={self.xs[0]}..{self.xs[1]},y={self.ys[0]}..{self.ys[1]},z={self.zs[0]}..{self.zs[1]}'


def parse_input(filename: str) -> List[Instruction]:
    instructions = []

    with open(filename) as f:
        for line in f:
            line = line.strip()

            m = p.match(line)
          
            xs = [int(m[2]), int(m[3])]
            ys = [int(m[4]), int(m[5])]
            zs = [int(m[6]), int(m[7])]

            assert (
                xs[0] < xs[1] and 
                ys[0] < ys[1] and 
                zs[0] < zs[1]
                )

            instruction = Instruction(operation=m[1], xs=xs, ys=ys, zs=zs)

            assert line == str(instruction)

            instructions.append(instruction)

    return instructions


def count(instructions):

    #TODO rename to all..
    #get sorted list of all coordinates

    xs = []
    for i in instructions:
        xs.extend([i.xs[0], i.xs[1]+1])

    ys = []
    for i in instructions:
        ys.extend([i.ys[0], i.ys[1]+1])

    zs = []
    for i in instructions:
        zs.extend([i.zs[0], i.zs[1]+1])

    xs.sort()
    ys.sort()
    zs.sort()

    sum = 0

    steps = len(xs)-1
    current_step = 0

    for x1,x2 in zip(xs, xs[1:]):

        x_inputs = [input for input in instructions if input.xs[0] <= x1 <= input.xs[1]]

        current_step += 1
        print(f'{(current_step / steps * 100):.2f}%')

        for y1,y2 in zip(ys, ys[1:]):

            xy_inputs = [input for input in x_inputs if input.ys[0] <= y1 <= input.ys[1]]
    
            for z1,z2 in zip(zs, zs[1:]):

                xyz_inputs = [input for input in xy_inputs if input.zs[0] <= z1 <= input.zs[1]]

                #order is preserved in list comprehensions so we should just be able to get the last one. 
                last_relevant_input = next(reversed(xyz_inputs), None)

                if last_relevant_input is not None and last_relevant_input.operation == 'on':
                    sum += (x2 - x1) * (y2 - y1) * (z2 - z1)
    
    return sum


def part1_instructions(instructions):
    part1_instructions = []

    for inst in instructions:
        if (
            (inst.xs[0] in range(-50, 51) and inst.xs[1] in range(-50, 51)) and 
            (inst.ys[0] in range(-50, 51) and inst.ys[1] in range(-50, 51)) and 
            (inst.zs[0] in range(-50, 51) and inst.zs[1] in range(-50, 51))
            ):
            part1_instructions.append(inst)
    
    return part1_instructions


#filename = '2021/22_input_example.txt'
filename = '2021/22_input.txt'
instructions = parse_input(filename)

print('Part 1:', count(part1_instructions(instructions))) #611176

print('Part 2:', count(instructions))

t2 = timer()
print(f'time: {(t2-t1):.4f}s')
