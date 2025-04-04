from typing import List
from diator.events import DomainEvent
from core.domain.kernel.entity import Entity


class ChessGameHistory(Entity):

    def __init__(self, history: List[DomainEvent]):
        super().__init__()
        self._gameHistory = history

    @staticmethod
    def empty():
        return ChessGameHistory([])

    def record(self, entry: DomainEvent):
        self._gameHistory.append(entry)

    def last(self):
        return self._gameHistory[:-1]

    def count(self):
        return len(self._gameHistory)

    def __iter__(self):
        return iter(self._gameHistory)