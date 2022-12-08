import numpy as np
from enum import Enum
import sys

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


# filename = "8/input"
filename = "8/example"
lines = []
with open(filename) as f:
    for line in f:
        lines.append([*(line.strip())])

arr_grid = np.array(lines, np.int32)
print(arr_grid.shape)


h = arr_grid.shape[0]
w = arr_grid.shape[1]

# Make 3d array. Add one dimention to the existing shape.
arr_visible = np.empty((4, h, w), dtype=bool)
arr_visible[::] = True

print(arr_grid)
print(arr_visible)

direction = LEFT
for row in range(h):
    highest = -1
    for col in range(w):
        curr = arr_grid[row, col]
        if col == 0:
            highest = curr
        else:
            curr = arr_grid[row, col]
            if curr > highest:
                highest = curr
            else:
                arr_visible[direction, row, col] = False

direction = RIGHT
for row in range(h):
    highest = -1
    for col in reversed(range(w)):
        curr = arr_grid[row, col]
        if col == 0:
            highest = curr
        else:
            curr = arr_grid[row, col]
            if curr > highest:
                highest = curr
            else:
                arr_visible[direction, row, col] = False

direction = DOWN
for col in range(w):
    highest = -1
    for row in range(h):
        curr = arr_grid[row, col]
        if col == 0:
            highest = curr
        else:
            curr = arr_grid[row, col]
            if curr > highest:
                highest = curr
            else:
                arr_visible[direction, row, col] = False

direction = UP
for col in range(w):
    highest = -1
    for row in reversed(range(h)):
        curr = arr_grid[row, col]
        if col == 0:
            highest = curr
        else:
            curr = arr_grid[row, col]
            if curr > highest:
                highest = curr
            else:
                arr_visible[direction, row, col] = False

print(
    "Part1:", np.count_nonzero(np.logical_or(np.logical_or(arr_visible[UP], arr_visible[DOWN]), np.logical_or(arr_visible[LEFT], arr_visible[RIGHT])))
)

# -----------------------------------------
