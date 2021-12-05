import common
import pandas as pd
import numpy as np
import re
from timeit import default_timer as timer

p = re.compile(r'(\d*),(\d*) -> (\d*),(\d*)')

def parse_input_df(lines):
    lines_lst = []
    for line in lines:
        m = p.match(line)

        x1 = m.group(1)
        y1 = m.group(2)
        x2 = m.group(3)
        y2 = m.group(4)

        lines_lst.append([ x1, y1, x2, y2 ])

    df = pd.DataFrame(lines_lst, columns=['x1', 'y1', 'x2', 'y2'])
    df = df.astype(int)

    return df

def create_ocean_floor_matrix(idf):

    max_x = idf[['x1', 'x2']].values.max()
    max_y = idf[['y1', 'y2']].values.max()
    
    mtx = np.zeros(shape=(max_x+1, max_y+1), dtype=np.int64)

    return mtx

def mark_vents(idf, mtx):
    for _, vent in idf.iterrows():
        x1 = vent.x1
        y1 = vent.y1
        x2 = vent.x2
        y2 = vent.y2

        inc_x = x2 - x1
        inc_x = inc_x if inc_x == 0 else inc_x // abs(inc_x)

        inc_y = y2 - y1 
        inc_y = inc_y if inc_y == 0 else inc_y // abs(inc_y)

        first = True

        x = x1
        y = y1

        while True:
            if first == True:
                first = False
            else:
                if x1 != x2:
                    x += inc_x
                if y1 != y2:
                    y += inc_y
                
            #increment matrix
            mtx[x,y] = mtx[x,y] + 1
            
            if x == x2 and y == y2:
                break

def challenge(filename):
    lines = common.read_file(filename)
    idf = parse_input_df(lines)
    mtx = create_ocean_floor_matrix(idf)

    #Part 1: only keep horizontal and vertical lines i.e. x1 = x2 or y1 = y2.
    fidf = idf[ (idf.x1 == idf.x2) | (idf.y1 == idf.y2) ]
    mtx_part1 = mtx.copy()    
    mark_vents(fidf, mtx_part1)

    count = mtx_part1[mtx_part1>=2].shape[0]
    print(f'Nr of points where at least two lines overlap: {count}')

    #Part 2: all of them
    mark_vents(idf, mtx)
    count = mtx[mtx>=2].shape[0]
    print(f'Nr of points where at least two lines overlap: {count}')

start = timer()
#challenge('2021/5_input_test.txt')
challenge('2021/5_input.txt')
end = timer()
print(end - start) 
