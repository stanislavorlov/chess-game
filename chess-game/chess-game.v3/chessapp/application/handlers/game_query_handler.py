from diator.events import Event
from diator.requests import RequestHandler
from chessapp.application.dtos.chess_game_dto import ChessGameDto
from chessapp.application.queries.chess_game_query import ChessGameQuery
from chessapp.infrastructure.mappers.dto_mapper import DtoMapper
from chessapp.infrastructure.repositories.chess_game_repository import ChessGameRepository


class ChessGameQueryHandler(RequestHandler[ChessGameQuery, ChessGameDto]):
    def __init__(self, repo: ChessGameRepository) -> None:
        self._repository = repo
        self._events: list[Event] = []

    @property
    def events(self) -> list[Event]:
        return self._events

    async def handle(self, request: ChessGameQuery) -> ChessGameDto:
        game = await self._repository.find(request.game_id.value)

        return DtoMapper.map_game(game)