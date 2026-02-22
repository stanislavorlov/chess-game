from typing import List
from ...domain.game.history_entry import ChessGameHistoryEntry
from ...domain.kernel.base import BaseEvent
from ...domain.kernel.entity import Entity
from ...domain.value_objects.history_entry_id import HistoryEntryId
from ...domain.events.piece_moved import PieceMoved


class ChessGameHistory(Entity):

    def __init__(self, history: List[ChessGameHistoryEntry]):
        super().__init__()
        self._gameHistory = history

    @staticmethod
    def empty():
        return ChessGameHistory([])

    def record(self, domain_event: BaseEvent, san: str = None):
        seq_number = len(self._gameHistory)
        entry = ChessGameHistoryEntry(HistoryEntryId.generate_id(), seq_number+1, domain_event, san)

        self._gameHistory.append(entry)

    def last(self):
        return self._gameHistory

    def count(self):
        return len(self._gameHistory)

    def __len__(self):
        return len(self._gameHistory)

    def moves_count(self):
        return len([entry for entry in self._gameHistory if isinstance(entry.history_event, PieceMoved)])

    def __iter__(self):
        self._gameHistory.sort(key=lambda entry: entry.sequence_number)

        return iter(self._gameHistory)