class Square:

    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col

    @property
    def col(self):
        return self._col

    @property
    def row(self):
        return self._row