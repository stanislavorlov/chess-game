from ...domain.game.chess_game import ChessGame
from ...infrastructure.models import GameDocument
from ...infrastructure.models.game_document import GameFormat, Players


class GameDocumentFactory:

    @staticmethod
    async def create(game: ChessGame) -> GameDocument:
        game_format = GameFormat(
            value=game.information.format.to_string(),
            time_remaining=game.information.format.time_remaining.main_string(),
            additional_time=game.information.format.time_remaining.additional_string()
        )
        players = Players(
            white_id=str(game.players.white),
            black_id=str(game.players.black)
        )

        new_game: GameDocument = GameDocument(
            _id=game.game_id.value,
            format=game_format,
            players=players,
            game_name=game.information.name,
            history=[]
        )

        return new_game