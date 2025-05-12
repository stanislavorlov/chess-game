from chessapp.domain.game.chess_game import ChessGame
from chessapp.domain.game.game_history import ChessGameHistory
from chessapp.domain.players.player_id import PlayerId
from chessapp.domain.players.players import Players
from chessapp.domain.value_objects.game_format import GameFormat
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.value_objects.game_information import GameInformation
from chessapp.infrastructure.models import GameDocument


class ChessGameFactory:

    @staticmethod
    async def create(document: GameDocument, history: ChessGameHistory) -> ChessGame:
        game_id: ChessGameId = ChessGameId(document.id)
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.parse_string(document.format.value, document.format.time_remaining,
                                              document.format.additional_time)
        game_info = GameInformation(game_format, document.date, document.game_name)

        return ChessGame(game_id, game_info, players, history)