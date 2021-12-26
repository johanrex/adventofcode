from dataclasses import dataclass
from os import name


#TODO varför slutar det fungera när man tar bort type hints???
@dataclass
class Player:
    name: str = None
    pos: int = None
    score: int = 0

#My input
p1 = Player(name='Player 1', pos=2)
p2 = Player(name='Player 2', pos=10)

#Test input
# p1 = Player(name='Player 1', pos=4)
# p2 = Player(name='Player 2', pos=8)

p1_turn = True

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

while p1.score < 1000 and p2.score < 1000:

    if p1_turn:
        p = p1
    else:
        p = p2

    vals = [get_die_val(), get_die_val(), get_die_val()]
    s = sum(vals)

    p.pos += s

    if p.pos % 10 == 0:
        p.pos = 10
    else:
        p.pos = p.pos % 10

    p.score += p.pos

    print(f'{p.name} rolls {"+".join(map(str, vals))} and moves to space {p.pos} for a total score of {p.score}.')

    #update player
    p1_turn = not p1_turn


print('part 1:', die_roll_counter * min(p1.score, p2.score)) # 571032

