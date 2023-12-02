from dataclasses import dataclass, field


RED = "red"
GREEN = "green"
BLUE = "blue"


@dataclass
class CubeInfo:
    color: str
    amount: int


@dataclass
class Handful:
    cube_infos: list[CubeInfo] = field(default_factory=list)


@dataclass
class GameInfo:
    game_id: str
    handfulls: list[Handful]

    def __str__(self) -> str:
        s = f"Game {self.game_id}: "
        for handful in self.handfulls:
            for cube_info in handful.cube_infos:
                s += f"{cube_info.amount} {cube_info.color}, "

            s = s[:-2]
            s += "; "

        s = s[:-2]
        return s


def parse(filename):
    game_infos = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            x = line.split(":")
            game_id = int(x[0].split()[1])
            rest = x[1]
            handfuls_str = rest.split(";")
            handfuls_str = [x.strip() for x in handfuls_str]
            handfuls = []
            for handful_str in handfuls_str:
                tokens = handful_str.split(",")
                tokens = [x.strip() for x in tokens]
                cube_infos = []
                for token in tokens:
                    amount, color = token.split()
                    cube_infos.append(CubeInfo(color, int(amount)))
                handfuls.append(Handful(cube_infos))

            game_infos.append(GameInfo(game_id, handfuls))

    return game_infos


def part1(game_infos):
    max_red = 12
    max_green = 13
    max_blue = 14

    game_id_sum = 0

    for gi in game_infos:
        valid = True
        for handful in gi.handfulls:
            for cube_info in handful.cube_infos:
                if cube_info.color == RED and cube_info.amount > max_red:
                    valid = False
                    break
                elif cube_info.color == GREEN and cube_info.amount > max_green:
                    valid = False
                    break
                elif cube_info.color == BLUE and cube_info.amount > max_blue:
                    valid = False
                    break
            if not valid:
                break

        if valid:
            game_id_sum += gi.game_id

    print("Part1", game_id_sum)


# filename = "2/example"
filename = "2/input"
game_infos = parse(filename)

for gi in game_infos:
    print(gi)

part1(game_infos)
