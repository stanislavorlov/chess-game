from core.domain.movements.delta.delta import Delta

class File:

    def __init__(self, file:str):
        self._start = 0
        self._end = 7

        if len(file) != 1 or file < 'a' or file > 'h':
            raise ValueError(f"Invalid file: '{file}'. Must be a letter between 'a' and 'h'.")
        self._file = file

    @property
    def file(self) -> str:
        """Returns the file as a string."""
        return self._file

    def to_index(self) -> int:
        """Converts the file to a 0-based index ('a' -> 0, ..., 'h' -> 7)."""
        return ord(self._file) - ord('a')

    @classmethod
    def from_index(cls, index: int):
        """Creates a File object from a 0-based index."""
        if index < 0 or index > 7:
            raise ValueError(f"Invalid index: '{index}'. Must be between 0 and 7.")
        file = chr(ord('a') + index)
        return cls(file)

    @classmethod
    def a(cls):
        return cls('a')

    @classmethod
    def b(cls):
        return cls('b')

    @classmethod
    def c(cls):
        return cls('c')

    @classmethod
    def d(cls):
        return cls('d')

    @classmethod
    def e(cls):
        return cls('e')

    @classmethod
    def f(cls):
        return cls('f')

    @classmethod
    def g(cls):
        return cls('g')

    @classmethod
    def h(cls):
        return cls('h')

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        return isinstance(other, File) and self._file == other._file

    def __str__(self) -> str:
        """String representation."""
        return self._file

    def __repr__(self) -> str:
        """Official representation."""
        return f"File('{self._file}')"

    def __iter__(self):
        return self

    def __next__(self):
        if self._start <= self._end:
            file = self.from_index(self._start)
            self._start += 1

            return file

        raise StopIteration

    def __sub__(self, other):
        if isinstance(other, File):
            return Delta(self.to_index() - other.to_index())

        raise Exception('Unsupported subtract operation')