from dataclasses import dataclass
import re
from collections import Counter
from PIL import Image
from tqdm import tqdm


@dataclass
class Robot:
    r: int
    c: int
    v_r: int
    v_c: int


def parse(filename: str):
    robots = []
    with open(filename) as f:
        for line in f:
            nrs = list(map(int, re.findall(r"-?\d+", line)))
            robot = Robot(nrs[1], nrs[0], nrs[3], nrs[2])
            robots.append(robot)
    return robots


def print_grid(robots: list[Robot], rows: int, cols: int):
    grid = [["." for _ in range(cols)] for _ in range(rows)]

    robot_positions = [(robot.r, robot.c) for robot in robots]
    counter = Counter(robot_positions)

    for r in range(rows):
        for c in range(cols):
            if (r, c) in counter:
                grid[r][c] = str(counter[(r, c)])

    for row in grid:
        print("".join(row))
    print("")


def move(robots: list[Robot], rows: int, cols: int):
    for robot in robots:
        robot.r += robot.v_r
        robot.c += robot.v_c

        # Wrap around if out of bounds
        if robot.r < 0:
            robot.r = rows + robot.r
        if robot.r >= rows:
            robot.r = robot.r - rows
        if robot.c < 0:
            robot.c = cols + robot.c
        if robot.c >= cols:
            robot.c = robot.c - cols


def quadrant_count(robots: list[Robot], rows: int, cols: int):
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for robot in robots:
        if robot.r == rows // 2 or robot.c == cols // 2:
            continue

        if robot.r < rows // 2 and robot.c < cols // 2:
            q1 += 1
        elif robot.r < rows // 2 and robot.c > cols // 2:
            q2 += 1
        elif robot.r > rows // 2 and robot.c < cols // 2:
            q3 += 1
        else:
            q4 += 1

    return q1, q2, q3, q4


# Create an image from a grid of pixels
def create_image(robots: list[Robot], rows, cols, second):
    grid = [["." for _ in range(cols)] for _ in range(rows)]

    for robot in robots:
        grid[robot.r][robot.c] = "1"

    image = Image.new("RGB", (cols, rows))
    pixels = image.load()

    for r in range(rows):
        for c in range(cols):
            pixels[c, r] = (0, 0, 0) if grid[r][c] == "." else (255, 255, 255)

    filename = f"day14/images/robots_{str(second).zfill(4)}.png"
    image.save(filename)


def solve(robots):
    for i in tqdm(range(10000), desc="Processing"):
        second = i + 1
        move(robots, rows, cols)

        q1, q2, q3, q4 = quadrant_count(robots, rows, cols)
        if any(q > sum([q1, q2, q3, q4]) - q for q in [q1, q2, q3, q4]):
            tqdm.write(f"At second {second}, one quadrant count is bigger than the other three combined.")
            print_grid(robots, rows, cols)
            break

        if second == 100:
            safety_factor = q1 * q2 * q3 * q4
            tqdm.write(f"Part 1: {safety_factor}")

        # create_image(robots, rows, cols, second)


# filename = "day14/example"
filename = "day14/input"

if "example" in filename:
    cols = 11
    rows = 7
else:
    cols = 101
    rows = 103

robots = parse(filename)
solve(robots)
