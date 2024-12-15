class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self._dict = dict()

    def is_within_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get(self, row, col, default_value: any = None):
        key = (row, col)
        if key not in self._dict:
            if default_value is not None:
                return default_value
            else:
                raise ValueError(f"Row {row} or col {col} is out of bounds")
        return self._dict[key]

    def set(self, row: int, col: int, value: any, allow_out_of_bounds: bool = False):
        if not allow_out_of_bounds and not self.is_within_bounds(row, col):
            raise ValueError(f"Row {row} or col {col} is out of bounds")

        key = (row, col)
        self._dict[key] = value

    def swap(self, a_row: int, a_col: int, b_row: int, b_col: int):
        a_key = (a_row, a_col)
        b_key = (b_row, b_col)

        self._dict[a_key], self._dict[b_key] = self._dict[b_key], self._dict[a_key]

    def print_grid(self):
        for row in range(self.rows):
            line = ""
            for col in range(self.cols):
                line += self.get(row, col)
            print(line)
