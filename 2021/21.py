from dataclasses import dataclass
from os import name


#TODO varför slutar det fungera när man tar bort type hints???
@dataclass
class Player:
    name: str = None
    pos: int = None
    score: int = 0

#My input
P1 = Player(name='Player 1', pos=2)
P2 = Player(name='Player 2', pos=10)

#Test input
# p1 = Player(name='Player 1', pos=4)
# p2 = Player(name='Player 2', pos=8)

P1_TURN = True

DIE_VAL = 0
DIE_ROLL_COUNTER = 0

def get_die_val():
    global DIE_VAL
    global DIE_ROLL_COUNTER

    DIE_ROLL_COUNTER += 1

    if DIE_VAL == 100:
        DIE_VAL = 1
    else:
        DIE_VAL += 1

    return DIE_VAL

while P1.score < 1000 and P2.score < 1000:

    if P1_TURN:
        p = P1
    else:
        p = P2

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
    P1_TURN = not P1_TURN


print('part 1:', DIE_ROLL_COUNTER * min(P1.score, P2.score)) # 571032

