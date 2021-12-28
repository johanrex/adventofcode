from __future__ import annotations
import itertools 
import functools


def smart_mod(n:int) -> int:
    return ((n-1) % 10)+1


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

#Test 444356092776315
p1_pos = 4
p2_pos = 8

print('Part 2:', max(part_2_wins(p1_pos, 0, p2_pos, 0)))
