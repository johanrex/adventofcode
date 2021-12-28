from __future__ import annotations
import itertools 
import functools

def weird_mod(n:int) -> int:
    while n > 10:
        n -= 10

    return n

def weird_mod2(n:int) -> int:
    if n % 10 == 0:
        n = 10
    else:
        n = n % 10
    return n

def weird_mod3(n:int) -> int:
    return ((n-1) % 10)+1


@functools.lru_cache(None)
def compute_wins(
    p1: int,
    p1_score: int,
    p2: int,
    p2_score: int
    ) -> tuple[int, int]:

    p1_wins = 0
    p2_wins = 0
    for i, j, k in itertools.product( (1,2,3), (1,2,3), (1,2,3) ):
        new_p1 = weird_mod(p1 + i + j + k)
        new_p1_score = p1_score + new_p1

        if new_p1_score >= 21:
            p1_wins += 1
        else:
            tmp_p2_wins, tmp_p1_wins = compute_wins(
                p2,
                p2_score, 
                new_p1,
                new_p1_score
            )
            p1_wins += tmp_p1_wins
            p2_wins += tmp_p2_wins

    return p1_wins, p2_wins


for i in range(12):
    print(weird_mod3(i))

p1 = 4
p2 = 8

print('Part 2:', compute_wins(p1, 0, p2, 0))