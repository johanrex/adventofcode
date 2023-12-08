from dataclasses import dataclass


@dataclass
class Card:
    id: int
    winning_nrs: list
    your_nrs: list


def parse(filename):
    cards = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            a, b = line.split(":")
            card_id = int(a.replace("Card ", ""))
            x, y = b.split("|")
            winning_nrs = [int(nr) for nr in x.split()]
            your_nrs = [int(nr) for nr in y.split()]
            cards.append(Card(card_id, winning_nrs, your_nrs))
    return cards


def matching_nrs(card):
    return set(card.winning_nrs) & (set(card.your_nrs))


def part1(cards):
    total_points = 0
    for card in cards:
        overlap = matching_nrs(card)

        if len(overlap) > 0:
            card_points = 2 ** (len(overlap) - 1)
            total_points += card_points

    assert 23441 == total_points
    print("Part 1:", str(total_points))


def part2(cards):
    total_cards = {card.id: 1 for card in cards}

    for card in cards:
        overlap = matching_nrs(card)
        if len(overlap) > 0:
            start = card.id + 1
            stop = start + len(overlap)
            for id in range(start, stop):
                total_cards[id] += total_cards[card.id]

    values = total_cards.values()
    s = sum(values)
    assert 5923918 == s
    print("Part 2:", s)


# filename = "4/example"
filename = "4/input"
cards = parse(filename)
part1(cards)
part2(cards)
print("Done")
