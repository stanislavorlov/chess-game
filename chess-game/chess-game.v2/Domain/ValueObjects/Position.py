from Domain.Kernel.ValueObject import ValueObject

class Position(ValueObject):
    def __init__(self, file: str, rank: str):
        self.file = file.lower() # Column ('a' to 'h')
        self.rank = rank.lower() # Row ('1' to '8')

    def __eq__(self, other):
        return self.file == other.file and self.rank == other.rank

    def __str__(self):
        return f"{self.file}{self.rank}"