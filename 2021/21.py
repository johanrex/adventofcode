from __future__ import annotations
from dataclasses import dataclass
import itertools
import functools

#Input: test. 
# p1_pos = 4
# p2_pos = 8

#Input: real. 
p1_pos = 2
p2_pos = 10

def smart_mod(n:int) -> int:
    return ((n-1) % 10)+1


#TODO varför slutar det fungera när man tar bort type hints???
@dataclass
class Player:
    name: str = None
    pos: int = None
    score: int = 0

p1 = Player(name='Player 1', pos=p1_pos)
p2 = Player(name='Player 2', pos=p2_pos)


die_val = 0
die_roll_counter = 0

def get_die_val():
    global die_val
    global die_roll_counter

    die_roll_counter += 1

    if die_val == 100:
        die_val = 1
    else:
        die_val += 1

    return die_val

def part1():
    p1_turn = True

    while p1.score < 1000 and p2.score < 1000:

        if p1_turn:
            p = p1
        else:
            p = p2

        vals = [get_die_val(), get_die_val(), get_die_val()]
        s = sum(vals)

        p.pos += s

        #smart mod
        p.pos = smart_mod(p.pos)
        
        p.score += p.pos

        print(f'{p.name} rolls {"+".join(map(str, vals))} and moves to space {p.pos} for a total score of {p.score}.')

        #update player
        p1_turn = not p1_turn

    return die_roll_counter * min(p1.score, p2.score)


@functools.lru_cache(None)
def part_2_wins(
    p1_pos: int,
    p1_score: int,
    p2_pos: int,
    p2_score: int
    ) -> tuple[int, int]:

    p1_wins = 0
    p2_wins = 0
    for i, j, k in itertools.product( (1,2,3), (1,2,3), (1,2,3) ):
        new_p1_pos = smart_mod(p1_pos + i + j + k)
        new_p1_score = p1_score + new_p1_pos

        if new_p1_score >= 21:
            p1_wins += 1
        else:
            tmp_p2_wins, tmp_p1_wins = part_2_wins(
                p2_pos,
                p2_score, 
                new_p1_pos,
                new_p1_score
            )
            p1_wins += tmp_p1_wins
            p2_wins += tmp_p2_wins

    return p1_wins, p2_wins

print('part 1:', part1()) # 571032

print('Part 2:', max(part_2_wins(p1_pos, 0, p2_pos, 0)))
# Test: Expected: 444356092776315 
# Real: Expected: 49975322685009
