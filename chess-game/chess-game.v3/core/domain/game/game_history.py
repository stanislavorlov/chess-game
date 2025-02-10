from typing import List

from core.domain.game.game_state import GameState
from core.domain.value_objects.side import Side

class ChessGameHistoryEntry:
    def __init__(self, current_side: Side, state: GameState):
        self._current_side = current_side
        self._state = state

class ChessGameHistory:

    def __init__(self, history: List[ChessGameHistoryEntry]):
        self._gameHistory = history

    @staticmethod
    def empty():
        return ChessGameHistory([])

    def record(self, entry: ChessGameHistoryEntry):
        self._gameHistory.append(entry)

    def last(self):
        return self._gameHistory[:-1]