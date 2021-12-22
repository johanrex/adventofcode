from collections import defaultdict
from dataclasses import dataclass
from typing import List
import re

#example 'on x=-10..44,y=-47..3,z=-30..20'
p = re.compile('(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')

@dataclass
class Instruction:
    operation: str
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    def __str__(self) -> str:
        return f'{self.operation} x={self.x[0]}..{self.x[1]},y={self.y[0]}..{self.y[1]},z={self.z[0]}..{self.z[1]}'


def parse_input(filename) -> List[Instruction]:
    instructions = []
    with open(filename) as f:
        for line in f:
            line = line.strip()

            m = p.match(line)

            #instructions.append(Instruction(operation=m[1], x=(int(m[2]), int(m[3])), y=(int(m[4]), int(m[5])), z=(int(m[6]), int(m[7]))))
            instructions.append(Instruction(operation=1 if m[1] == 'on' else 0, x=(int(m[2]), int(m[3])), y=(int(m[4]), int(m[5])), z=(int(m[6]), int(m[7]))))

    return instructions


def do_instruction(inst):

    for x in range(inst.x[0], inst.x[1]+1):
        for y in range(inst.y[0], inst.y[1]+1):
            for z in range(inst.z[0], inst.z[1]+1):
                key = f'{x},{y},{z}'

                if inst.operation == 1:
                    cube[key] = inst.operation
                else:
                    if key in cube:
                        del cube[key]


#filename = '2021/22_input_example.txt'
filename = '2021/22_input.txt'
instructions = parse_input(filename)

print('Nr of instructions:', len(instructions))

cube = {}

for i, inst in enumerate(instructions):
    if (
        (inst.x[0] in range(-50, 51) and inst.x[1] in range(-50, 51)) and 
        (inst.y[0] in range(-50, 51) and inst.y[1] in range(-50, 51)) and 
        (inst.z[0] in range(-50, 51) and inst.z[1] in range(-50, 51)) 
    ):
        print('Executing instruction:', i+1)
        do_instruction(inst)
    else:
        print('skipping:', str(inst))
        continue


print('Part 1:', len(cube)) #611176

