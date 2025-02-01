from core.domain.game.chess_game import ChessGame
from core.domain.game.game_format import GameFormat
from core.domain.game.game_state import GameState
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.side import Side


class ChessGameFactory:

    @staticmethod
    def start_new(player_side: Side, game_format: GameFormat):
        return ChessGame(ChessGameId.generate_id(), player_side, GameState(), game_format)