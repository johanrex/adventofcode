from grid import Grid

p1 = Grid.Pos(1, 2)
p2 = Grid.Pos(1, 3)

assert set([p1, p1, p2, p2]) == {p1, p2}
