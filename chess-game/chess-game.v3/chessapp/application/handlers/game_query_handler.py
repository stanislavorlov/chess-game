from dataclasses import dataclass

from chessapp.application.dtos.chess_game_dto import ChessGameDto
from chessapp.application.handlers.base_query_handler import BaseQueryHandler
from chessapp.application.queries.chess_game_query import ChessGameQuery
from chessapp.infrastructure.mappers.dto_mapper import DtoMapper
from chessapp.infrastructure.repositories.chess_game_repository import ChessGameRepository


@dataclass(frozen=True, kw_only=True)
class ChessGameQueryHandler(BaseQueryHandler[ChessGameQuery, ChessGameDto]):
    repository: ChessGameRepository

    async def handle(self, request: ChessGameQuery) -> ChessGameDto:
        game = await self.repository.find(request.game_id.value)

        return DtoMapper.map_game(game)