from collections import defaultdict

from core.domain.game.chess_game import ChessGame
from core.domain.value_objects.game_id import ChessGameId


class ChessGameRepository:

    def __init__(self):
        self._games = defaultdict()

    def save(self, game: ChessGame):
        self._games[game.game_id] = game

    def get(self, game_id: ChessGameId):
        return self._games[game_id]