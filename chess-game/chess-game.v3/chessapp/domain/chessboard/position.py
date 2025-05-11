from chessapp.domain.chessboard.file import File
from chessapp.domain.chessboard.rank import Rank


class Position:

    def __init__(self, file: File, rank: Rank):
        self._file = file
        self._rank = rank

    def __eq__(self, other):
        if isinstance(other, Position):
            return self._file == other._file and self._rank == other._rank

        return False

    def __str__(self):
        return f"{self._file}{self._rank}"

    def __hash__(self):
        return hash(str(self._file) + str(self._rank))

    @property
    def file(self) -> File:
        return self._file

    @property
    def rank(self) -> Rank:
        return self._rank

    @staticmethod
    def parse(value: str):
        file, rank = value[0], value[1]

        return Position(File(file), Rank(int(rank)))
