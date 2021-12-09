import numpy as np
import common

def read_input(filename):
    inputs = []
    with(open(filename, "r")) as f:
        for line in f:
            row = list(line.strip())
            inputs.append(row)

    mtx = np.asarray(inputs, np.int8)
    return mtx

def get_smallest_points(mtx):
    smallest_points = []
    rows, cols = mtx.shape
    for row in range(1, rows-1):
        for col in range(1, cols-1):

            val = mtx[row,col]

            #is smaller than adjacent?
            if (
                val < mtx[row-1,col] and 
                val < mtx[row+1,col] and 
                val < mtx[row,col-1] and 
                val < mtx[row,col+1]
            ):
                smallest_points.append( (row,col) )

    return smallest_points

def flood_fill(row, col, mtx):

    nr_of_rows = mtx.shape[0]
    nr_of_rows = mtx.shape[1]

    points_affected = 0

    if mtx[row,col] != -1 and mtx[row,col] < 9:

        #use -1 to indicate visited
        mtx[row,col] = -1
        points_affected = 1

        if row > 0:
            points_affected += flood_fill(row-1,col, mtx)
        if row < nr_of_rows - 1:
            points_affected += flood_fill(row+1,col, mtx)
        if col > 0:
            points_affected += flood_fill(row,col-1, mtx)
        if row < nr_of_rows -1:
            points_affected += flood_fill(row,col+1, mtx)

    return points_affected

def part1(smallest_points, mtx):
    s = 0

    #TODO how to extract elements from array without loop?
    for point in smallest_points:
        s += mtx[point]+1

    print(f'Part 1. Sum: {s}.')

def part2(smallest_points, mtx):

    basin_sizes = []
    for low_point in smallest_points:
        row = low_point[0]
        col = low_point[1]
        size = flood_fill(row,col, mtx)
        basin_sizes.append(size)

    s = np.prod(sorted(basin_sizes, reverse=True)[:3])
    print(f'Part 2. Sum: {s}.')

@common.timed
def challenge(filename):

    mtx = read_input(filename)

    #pad with bigger value outside for gloriously easy manipulation. 
    mtx = np.pad(mtx, 1, constant_values=10)

    #common input to both parts
    smallest_points = get_smallest_points(mtx)


    part1(smallest_points, mtx)
    part2(smallest_points, mtx)

#filename = '2021/9_input_example.txt'
filename = '2021/9_input.txt'

challenge(filename)
