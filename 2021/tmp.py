from time import perf_counter as pfc
from heapq import heappush, heappop


def read_puzzle(filename):
    with open(filename) as f:
        return "".join([c for row in f.read().split("\n") for c in row if c not in "# "])


def can_leave_room(room, puzzle, part1):
    t = targets1 if part1  else targets2
    memb = {puzzle[i] for i in t[room]}
    if memb in ({'.'}, {'.',room}, {room}): return False
    for i in t[room]:
        if puzzle[i] != '.': return i    


def can_enter_room(i1,amphi, puzzle, part1):
    t = targets1 if part1  else targets2
    bestI = False
    for i in t[amphi]:
        if puzzle[i] == ".": bestI = i
        elif puzzle[i] != amphi: return False
    if not blocked(i1, stepout[amphi], puzzle): return bestI


def blocked(i1, i2, puzzle):
    step = 1 if i1 < i2 else -1
    return any(puzzle[v] != "." for v in range(i1 + step, i2 + step, step))


def get_possible_hallway_pos(i1, puzzle):
    for i2 in hallway:
        if puzzle[i2] != ".": continue
        if blocked(stepout[targetsI[i1]], i2, puzzle): continue
        yield i2


def distance(i1, i2):
    if i1 > i2: i1,i2 = i2,i1
    return abs(stepout[targetsI[i2]] - i1) + (i2-7)//4


def swap(i1, i2, puzzle):
    p = list(puzzle)
    p[i1], p[i2] = p[i2], p[i1]
    return "".join(p)


def possible_moves(puzzle,part1):
    moves = []
    for i1 in hallway:
        if puzzle[i1] == ".": continue
        if not (i2 := can_enter_room(i1,puzzle[i1], puzzle, part1)): continue
        moves.append((i1, i2, distance(i1, i2)))
    for room in "ABCD":
        if not (i1 := can_leave_room(room, puzzle, part1)): continue
        for i2 in get_possible_hallway_pos(i1, puzzle):
            moves.append((i1, i2, distance(i1, i2)))
    return moves


def solve(puzzle,part1=True):
    queue, seen = [(0, puzzle)], {puzzle: 0}
    solution = '.'*11+'ABCD'*2 if part1 else '.'*11+'ABCD'*4
    while queue:
        cost, state = heappop(queue)
        if state == solution: return cost
        for i1, i2, dist in possible_moves(state,part1):
            new_cost = cost + dist * energy[state[i1]]
            moved = swap(i1, i2, state)
            if seen.get(moved, 999999) <= new_cost: continue
            seen[moved] = new_cost
            heappush(queue, (new_cost, moved))


energy = dict(A=1, B=10, C=100, D=1000)
hallway = {0, 1, 3, 5, 7, 9, 10}
stepout = {"A": 2, "B": 4, "C": 6, "D": 8}
targets1 = {"A": range(11,16,4), "B": range(12,17,4), "C": range(13,18,4), "D": range(14,19,4)}
targets2 = {"A": range(11,24,4), "B": range(12,25,4), "C": range(13,26,4), "D": range(14,27,4)}
targetsI = {v: key for key, val in targets2.items() for v in val}


start = pfc()
print(solve(read_puzzle("2021/23_input.txt")))
#print(solve(read_puzzle("Tag_23_b.txt"),False))
print(pfc() - start)