from dataclasses import dataclass
from enum import Enum, unique
from typing import Literal
import bitstring
from typing import List

#filename = '2021/16_input_example.txt'
filename = '2021/16_input.txt'

class Packet:
    def __init__(self):

        self.version: int
        self.type: int
        self.value: int
        self.sub_packets: List[Packet] = []

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

#print packets
for packet in packets:
    print(repr(packet))


print('part1:', sum_versions(packets))
i = 0
