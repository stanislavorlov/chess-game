from core.domain.game.chess_game import ChessGame
from core.domain.game.game_format import GameFormat
from core.domain.game.game_state import GameState
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.infrastructure.models import GameDocument


class ChessGameFactory:

    @staticmethod
    def start_new(players: Players, game_format: GameFormat):
        game_id = ChessGameId.generate_id()
        game_state = GameState(game_id)

        return ChessGame(game_id, players, game_state, game_format)