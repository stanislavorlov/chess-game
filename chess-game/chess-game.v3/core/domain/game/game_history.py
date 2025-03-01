from typing import List
from diator.events import DomainEvent

class ChessGameHistory:

    def __init__(self, history: List[DomainEvent]):
        self._gameHistory = history

    @staticmethod
    def empty():
        # ToDo: list of PiecePositioned events ??

        return ChessGameHistory([])

    def record(self, entry: DomainEvent):
        self._gameHistory.append(entry)

    def last(self):
        return self._gameHistory[:-1]

    def __iter__(self):
        return iter(self._gameHistory)