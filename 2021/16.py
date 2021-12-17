from dataclasses import dataclass
from enum import Enum, unique
from typing import Literal
import bitstring

filename = '2021/16_input_example.txt'


class Packet:
    def __init__(self):
        self.version: int
        self.type: int
        self.value: int

def parse_literal(bs):
    val = 0
    done = False
    while not done:
        tmp = bs.read('uint:5')

        if tmp & 1<<4:
            tmp &= ~(1<<4) #remove group indicator
        else:
            done = True
        val += tmp

        if not done:
            val = val << 4

    align = 4 - (bs.pos % 4)
    bs.read(align)


with open(filename, 'r') as f:
    line = f.readline().strip()

input = bytearray.fromhex(line)

bs = bitstring.ConstBitStream(input)

packets = []
p = None
while True:
    if p == None:
        p = Packet()
        p.version = bs.read('uint:3')
        p.type = bs.read('uint:3')

    if p.type == 4: #literal value
        val = parse_literal(bs)
        p.value = val
        packets.append(p)
        p = None
    else: 
        #operator
        length_type_id = bs.read('uint:1')
        if length_type_id == 0:
            #15 bits...
            length_of_subpackets = bs.read('uint:15')
            pass
        elif length_type_id == 1:
            #11 bits
            nr_of_subpackets = bs.read('uint:11')
            pass
        else:
            raise Exception('unexpected')



# for b in input:
#     pass

i = 0