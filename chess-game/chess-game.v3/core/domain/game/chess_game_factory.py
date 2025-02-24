from core.domain.game.chess_game import ChessGame
from core.domain.game.game_format import GameFormat
from core.domain.game.game_history import ChessGameHistory
from core.domain.game.game_initialization import GameInitialization
from core.domain.value_objects.game_id import ChessGameId


class ChessGameFactory:

    @staticmethod
    def start_new(game_format: GameFormat):
        game_id = ChessGameId.generate_id()

        chess_game = ChessGame(game_id, game_format, ChessGameHistory.empty())
        chess_game.raise_events(GameInitialization.init())

        return chess_game