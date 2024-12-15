from dataclasses import dataclass
import functools
from collections import defaultdict


class Grid:
    @dataclass(frozen=True, eq=True)
    @functools.total_ordering
    class Pos:
        __slots__ = ("row", "col")

        row: int
        col: int

        def __lt__(self, other):
            if not isinstance(other, Grid.Pos):
                return NotImplemented

            if self.row == other.row:
                return self.col < other.col

            return self.row < other.row

        def __add__(self, other):
            if not isinstance(other, Grid.Pos):
                return NotImplemented
            return Grid.Pos(self.row + other.row, self.col + other.col)

        def __sub__(self, other):
            if not isinstance(other, Grid.Pos):
                return NotImplemented
            return Grid.Pos(self.row - other.row, self.col - other.col)

    def __init__(self, rows: int, cols: int, default_value: any = None):
        self.rows = rows
        self.cols = cols
        self._dict = defaultdict(lambda: default_value)

    def is_pos_within_bounds(self, pos: Pos) -> bool:
        return 0 <= pos.row < self.rows and 0 <= pos.col

    def is_within_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get(self, row, col, default_value: any = None):
        pos = Grid.Pos(row, col)
        return self.get_by_pos(pos, default_value)

    def get_by_pos(self, pos: Pos, default_value: any = None):
        if pos.row < 0 or pos.row >= self.rows or pos.col < 0 or pos.col >= self.cols:
            if default_value is not None:
                return default_value
            else:
                raise ValueError(f"Row {pos.row} or col {pos.col} is out of bounds")

        return self._dict[pos]

    def set_by_pos(self, pos: Pos, value: any) -> bool:
        if pos.row < 0 or pos.row >= self.rows or pos.col < 0 or pos.col >= self.cols:
            return False
        self._dict[pos] = value

    def set(self, row: int, col: int, value: any) -> bool:
        pos = Grid.Pos(row, col)
        return self.set_by_pos(pos, value)

    def swap_by_pos(self, a: Pos, b: Pos):
        self._dict[a], self._dict[b] = self._dict[b], self._dict[a]

    def swap(self, a_row: int, a_col: int, b_row: int, b_col: int):
        a_pos = Grid.Pos(a_row, a_col)
        b_pos = Grid.Pos(b_row, b_col)

        self.swap_by_pos(a_pos, b_pos)

    def print_grid(self):
        for row in range(self.rows):
            line = ""
            for col in range(self.cols):
                line += self.get(row, col)
            print(line)
