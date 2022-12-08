import numpy as np

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


filename = "8/input"
# filename = "8/example"
lines = []
with open(filename) as f:
    for line in f:
        lines.append([*(line.strip())])

arr_grid = np.array(lines, np.int32)

h = arr_grid.shape[0]
w = arr_grid.shape[1]

# Make 3d array. Add one dimention to the existing shape.
arr_visible = np.empty((4, h, w), dtype=bool)
arr_visible[::] = True

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

arr_scenic_dist = np.empty((4, h, w), int)
arr_scenic_dist[::] = 0

for row in range(h):
    for col in range(w):
        curr = arr_grid[row, col]

        # LEFT
        scenic_dist = 0
        for other_col in range(col + 1, w):
            other = arr_grid[row, other_col]
            if other > curr:
                break
            else:
                scenic_dist += 1
                if other == curr:
                    break
        arr_scenic_dist[LEFT, row, col] = scenic_dist

        # RIGHT
        scenic_dist = 0
        for other_col in reversed(range(0, col)):
            other = arr_grid[row, other_col]
            if other > curr:
                break
            else:
                scenic_dist += 1
                if other == curr:
                    break
        arr_scenic_dist[RIGHT, row, col] = scenic_dist

        # DOWN
        scenic_dist = 0
        for other_row in range(row + 1, h):
            other = arr_grid[other_row, col]
            if other > curr:
                break
            else:
                scenic_dist += 1
                if other == curr:
                    break
        arr_scenic_dist[DOWN, row, col] = scenic_dist

        # UP
        scenic_dist = 0
        for other_row in reversed(range(0, row)):
            other = arr_grid[other_row, col]
            if other > curr:
                break
            else:
                scenic_dist += 1
                if other == curr:
                    break
        arr_scenic_dist[UP, row, col] = scenic_dist

print("Part2:", np.max(arr_scenic_dist[DOWN] * arr_scenic_dist[UP] * arr_scenic_dist[LEFT] * arr_scenic_dist[RIGHT]))
