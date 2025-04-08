from core.domain.movements.delta.delta import Delta


class Rank:
    _valid_ranks = range(0, 8)  # Valid ranks are integers from 0 to 7

    def __init__(self, rank: int):
        self._start = 0
        self._end = 7

        # Validate that the rank is between 1 and 8
        if rank not in Rank._valid_ranks:
            raise ValueError(f"Invalid rank: '{rank}'. Must be an integer between 0 and 7.")
        self._rank = rank

    @property
    def value(self) -> int:
        """Returns the rank as an integer."""
        return self._rank + 1

    def to_index(self) -> int:
        return self._rank

    @classmethod
    def from_index(cls, index: int):
        """Creates a Rank object from an integer index."""
        if index < 0 or index > 7:
            raise ValueError(f"Invalid index: '{index}'. Must be between 0 and 7.")
        return cls(index)

    # Class-level properties for ranks 1 to 8
    @classmethod
    def r1(cls):
        return cls(0)

    @classmethod
    def r2(cls):
        return cls(1)

    @classmethod
    def r3(cls):
        return cls(2)

    @classmethod
    def r4(cls):
        return cls(3)

    @classmethod
    def r5(cls):
        return cls(4)

    @classmethod
    def r6(cls):
        return cls(5)

    @classmethod
    def r7(cls):
        return cls(6)

    @classmethod
    def r8(cls):
        return cls(7)

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        return isinstance(other, Rank) and self._rank == other._rank

    def __str__(self) -> str:
        """String representation."""
        return str(self._rank)

    def __repr__(self) -> str:
        """Official representation."""
        return f"Rank({self._rank})"

    def __iter__(self):
        return self

    def __next__(self):
        if self._start <= self._end:
            rank = self.from_index(self._start)
            self._start += 1

            return  rank

        raise StopIteration

    def __sub__(self, other):
        if isinstance(other, Rank):
            return Delta(self._rank - other._rank)

        raise Exception('Unsupported subtract operation')

    def __lt__(self, other):
        if isinstance(other, Rank):
            return self._rank < other._rank

        raise Exception('Unsupported less than operation')

    def __le__(self, other):
        if isinstance(other, Rank):
            return self._rank <= other._rank

        raise Exception('Unsupported less than or equal operation')

    def __gt__(self, other):
        if isinstance(other, Rank):
            return self._rank > other._rank

        raise Exception('Unsupported greater than operation')

    def __ge__(self, other):
        if isinstance(other, Rank):
            return self._rank >= other._rank

        raise Exception('Unsupported greater than or equal operation')