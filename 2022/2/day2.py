matches = []
with open("2/input") as f:
    for line in f:
        matches.append((line[0], line[2]))

mapper = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "R",
    "Y": "P",
    "Z": "S",
}

moves = ["R", "S", "P"]


def get_winning_move(m):
    return moves[moves.index(m) - 1]


def get_losing_move(m):
    return moves[(moves.index(m) + 1) % 3]


def score_match(p1, p2):
    """
    Rock defeats Scissors,
    Scissors defeats Paper,
    Paper defeats Rock.
    If both players choose the same shape, the round instead ends in a draw.

    Score: (1 for Rock, 2 for Paper, and 3 for Scissors)
    plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).
    """
    score = 0

    # Shape:
    if p2 == "R":
        score += 1
    elif p2 == "P":
        score += 2
    elif p2 == "S":
        score += 3

    # Outcome:
    if p1 == p2:
        score += 3
    elif (p2 == "R" and p1 == "S") or (p2 == "S" and p1 == "P") or (p2 == "P" and p1 == "R"):
        score += 6

    return score


def score_part1(matches):
    score = 0
    for match in matches:
        p1, p2 = match
        p1 = mapper[p1]
        p2 = mapper[p2]

        score += score_match(p1, p2)

    return score


def score_part2(matches):

    score = 0
    for match in matches:
        p1, p2 = match
        p1 = mapper[p1]

        # X means you need to lose,
        # Y means you need to end the round in a draw, and
        # Z means you need to win.
        if p2 == "X":
            p2 = get_losing_move(p1)
        elif p2 == "Y":
            p2 = p1
        elif p2 == "Z":
            p2 = get_winning_move(p1)

        score += score_match(p1, p2)

    return score


s = score_part1(matches)
assert s == 11841
print("part1:", s)  # 11841

s = score_part2(matches)
assert s == 13022
print("part2:", s)  # 13022
