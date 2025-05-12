from chessapp.domain.game.chess_game import ChessGame
from chessapp.infrastructure.models import GameDocument
from chessapp.infrastructure.models.game_document import GameState, GameFormat, Players


class GameDocumentFactory:

    @staticmethod
    async def create(game: ChessGame) -> GameDocument:
        game_state = GameState(
            turn=str(game.game_state.turn),
        )
        game_format = GameFormat(
            value=game.information.format.to_string(),
            time_remaining=game.information.format.time_remaining.main_string(),
            additional_time=game.information.format.time_remaining.additional_string()
        )
        players = Players(
            white_id='',
            black_id=''
        )
        new_game: GameDocument = GameDocument(
            _id=game.game_id.value,
            date=game.information.date,
            state=game_state,
            format=game_format,
            players=players,
            result='',
            game_name=game.information.name
        )

        return new_game