from core.domain.game.chess_game import ChessGame
from core.domain.game.game_format import GameFormat
from core.domain.game.game_state import GameState
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.infrastructure.models import GameDocument


class ChessGameFactory:

    @staticmethod
    def domain_to_collection(game: ChessGame) -> GameDocument:
        pass

    @staticmethod
    def collection_to_domain(document: GameDocument) -> ChessGame:
        game_id: ChessGameId = ChessGameId(document.game_id)
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        state = GameState(game_id)
        game_format = GameFormat.from_string(document.format.value, document.format.time_remaining)

        return ChessGame(game_id, players, state, game_format)