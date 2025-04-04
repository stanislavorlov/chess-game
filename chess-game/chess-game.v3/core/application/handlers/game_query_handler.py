from diator.events import Event
from diator.requests import RequestHandler

from core.application.queries.chess_game_query import ChessGameQuery
from core.application.responses.create_game_result import ChessGameQueryResult, GameStateQueryResult, \
    GameFormatQueryResult, PlayersQueryResult
from core.domain.chessboard.board import Board
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class ChessGameQueryHandler(RequestHandler[ChessGameQuery, ChessGameQueryResult]):
    def __init__(self, repo: ChessGameRepository) -> None:
        self._repository = repo
        self._events: list[Event] = []

    @property
    def events(self) -> list[Event]:
        return self._events

    async def handle(self, request: ChessGameQuery) -> ChessGameQueryResult:
        game = await self._repository.find_by_id(request.game_id)

        state_result = GameStateQueryResult(
            turn = game.game_state.turn.value(),
            started = game.game_state.is_started,
            finished = game.game_state.is_finished
        )

        format_result = GameFormatQueryResult(
            value = game.information.format.to_string(),
            remaining_time = game.information.format.time_remaining.main_time,
            additional_time = game.information.format.time_remaining.additional_time,
        )

        players_result = PlayersQueryResult(
            white_id = str(game.players.white),
            black_id = str(game.players.black)
        )

        board = Board()
        board.reply(game.history)

        print('Game history count:')
        print(game.history.count())

        return ChessGameQueryResult(
            game_id=game.game_id.value,
            date=game.information.date,
            name=game.information.name,
            state=state_result,
            game_format=format_result,
            players=players_result,
        )