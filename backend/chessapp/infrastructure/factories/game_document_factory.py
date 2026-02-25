from ...domain.game.chess_game import ChessGame
from ...infrastructure.models import GameDocument
from ...infrastructure.models.game_document import GameFormat, Players


class GameDocumentFactory:

    @staticmethod
    async def create(game: ChessGame) -> GameDocument:
        game_format = GameFormat(
            value=game.information.format.to_string(),
            time_remaining=game.information.format.time_remaining.base_time_string(),
            move_increment=game.information.format.time_remaining.move_increment_string()
        )
        players = Players(
            white_id=str(game.players.white),
            black_id=str(game.players.black)
        )

        new_game: GameDocument = GameDocument(
            _id=game.game_id.value,
            format=game_format,
            players=players,
            status=str(game.game_state.status),
            white_remaining_time=game.white_timer,
            black_remaining_time=game.black_timer,
            game_name=game.information.name,
            history=[]
        )

        return new_game