from dataclasses import dataclass
import time
import math
import re
import copy
from collections import Counter
import sys
import os
from collections import defaultdict
import itertools

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid
import utils.parse_utils as parse_utils


def part1(data):
    print("Part 1:", -1)


def part2(data):
    print("Part 2:", -1)


filename = "dayX/example"
# filename = "dayX/input"

data = parse_utils.parse_ints(filename)
part1(data)
part2(data)
