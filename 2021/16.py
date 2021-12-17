from dataclasses import dataclass
from enum import Enum, unique
from typing import Literal
import bitstring
from typing import List
import math

#filename = '2021/16_input_example.txt'
filename = '2021/16_input.txt'

class Packet:
    def __init__(self):

        self.version: int
        self.type: int
        self.value: int
        self.sub_packets: List[Packet] = []

    def eval(self):
        if self.type == 4: #literal
            return self.value
        elif self.type == 0: # sum
            return sum([sub.eval() for sub in self.sub_packets])
        elif self.type == 1: # product
            return math.prod([sub.eval() for sub in self.sub_packets])
        elif self.type == 2: # min
            return min([sub.eval() for sub in self.sub_packets])
        elif self.type == 3: # max
            return max([sub.eval() for sub in self.sub_packets])
        elif self.type == 5: # >
            return 1 if self.sub_packets[0].eval() > self.sub_packets[1].eval() else 0
        elif self.type == 6: # <
            return 1 if self.sub_packets[0].eval() < self.sub_packets[1].eval() else 0
        elif self.type == 7: # <
            return 1 if self.sub_packets[0].eval() == self.sub_packets[1].eval() else 0
        else:
            raise Exception('unexpected')


    def __repr__(self) -> str:

        s = f'version:{self.version}, type:{self.type}'
        if self.type == 4:
            s += f',value:{self.value}'
        else:
            for sub_packet in self.sub_packets:
                s += '\n'
                s += f'{repr(sub_packet)}'

        return s

def read_header(bs):
    
    #6 bits in header
    version = bs.read('uint:3')
    type = bs.read('uint:3')

    return version, type

def parse_literal(bs, version, type):

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

    p = Packet()
    p.version = version
    p.type = type
    p.value = val

    return p

def parse_operator(bs, version, type):

    p = Packet()
    p.version = version
    p.type = type

    length_type_id = bs.read('uint:1')

    if length_type_id == 0:

        #15 bits...
        length_of_subpackets = bs.read('uint:15')

        sub_packets_end_pos = bs.pos + length_of_subpackets

        while bs.pos < sub_packets_end_pos:
            p.sub_packets.append(parse_packet(bs))
        
    elif length_type_id == 1:

        #11 bits
        nr_of_subpackets = bs.read('uint:11')

        for _ in range(nr_of_subpackets):
            p.sub_packets.append(parse_packet(bs))

    else:
        raise Exception('unexpected')

    return p


def parse_packet(bs):
    version, type = read_header(bs)

    if type == 4: #literal value
        return parse_literal(bs, version, type)
    else: 
        return parse_operator(bs, version, type)


def sum_versions(packets):
    sum = 0
    for packet in packets:
        sum += packet.version
        sum += sum_versions(packet.sub_packets)

    return sum
       

with open(filename, 'r') as f:
    line = f.readline().strip()

input = bytearray.fromhex(line)

bs = bitstring.ConstBitStream(input)

packets = []

#Parse all packets
while bs.pos < bs.length - 7:

    p = parse_packet(bs)

    if p is not None:
        packets.append(p)

if len(packets) != 1:
    raise Exception('unexpected')

#print packets
# for packet in packets:
#     print(repr(packet))


print('part1:', sum_versions(packets))
print('part2:', packets[0].eval())

i = 0
