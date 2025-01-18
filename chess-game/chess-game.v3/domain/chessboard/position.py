class Position:

    def __init__(self, file: str, rank: str):
        self._file = file
        self._rank = rank

    def __eq__(self, other):
        if isinstance(other, Position):
            return self._file == other._file and self._rank == other._rank

        return  False

    def __str__(self):
        return f"{self._file}{self._rank}"