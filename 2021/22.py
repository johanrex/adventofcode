import re

#example 'on x=-10..44,y=-47..3,z=-30..20'
p = re.compile('(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')

with open('2021/22_input.txt') as f:
    for line in f:
        line = line.strip()

        m = p.match(line)

        operator = m[1]

        x_from = int(m[2])
        x_to = int(m[3])

        y_from = int(m[4])
        y_to = int(m[5])

        z_from = int(m[6])
        z_to = int(m[7])

        tmp = f'{operator} x={x_from}..{x_to},y={y_from}..{y_to},z={z_from}..{z_to}'

        assert line == tmp
    
print('done')

