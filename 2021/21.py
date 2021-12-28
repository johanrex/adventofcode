from dataclasses import dataclass
import itertools

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
        p.pos = ((p.pos-1) % 10)+1

        p.score += p.pos

        print(f'{p.name} rolls {"+".join(map(str, vals))} and moves to space {p.pos} for a total score of {p.score}.')

        #update player
        p1_turn = not p1_turn

    return die_roll_counter * min(p1.score, p2.score)

print('part 1:', part1()) # 571032


def part2():
    die_combinations = list(itertools.permutations([1,2,3], 3))

    P1_SCORE_IDX = 0
    P2_SCORE_IDX = 1
    P1_POS_IDX = 2
    P2_POS_IDX = 3
    DIE_ROLL_COUNTER = 4

    state = [0]*5

    show_must_go_on = True
    p1_turn = True

    while show_must_go_on:
        if p1_turn:
            key_score = 'p1.score'
            key_pos = 'p1.pos'
        else:
            key_score = 'p2.score'
            key_pos = 'p2.pos'

        for die_result in die_combinations:
            s = sum(die_result)
            state[key_pos] += s

            if state[key_pos] % 10 == 0:
                state[key_pos] = 10
            else:
                state[key_pos] = state[key_pos] % 10

            state[key_score] += state[key_pos]

    #update player
    p1_turn = not p1_turn

#part 2
#p1.score, p2.score, p1.pos, p2.pos, die_roll_counter

