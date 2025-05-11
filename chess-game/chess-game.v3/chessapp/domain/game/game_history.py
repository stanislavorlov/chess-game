from typing import List
from diator.events import DomainEvent
from chessapp.domain.game.history_entry import ChessGameHistoryEntry
from chessapp.domain.kernel.entity import Entity
from chessapp.domain.value_objects.history_entry_id import HistoryEntryId


class ChessGameHistory(Entity):

    def __init__(self, history: List[ChessGameHistoryEntry]):
        super().__init__()
        self._gameHistory = history

    @staticmethod
    def empty():
        return ChessGameHistory([])

    def record(self, domain_event: DomainEvent):
        seq_number = len(self._gameHistory)
        entry = ChessGameHistoryEntry(HistoryEntryId.empty(), seq_number+1, domain_event)

        self._gameHistory.append(entry)

    def last(self):
        return self._gameHistory[:-1]

    def count(self):
        return len(self._gameHistory)

    def __iter__(self):
        self._gameHistory.sort(key=lambda entry: entry.sequence_number)

        return iter(self._gameHistory)