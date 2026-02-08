from dataclasses import dataclass

from ...application.dtos.chess_game_dto import ChessGameDto
from ...application.handlers.base_query_handler import BaseQueryHandler
from ...application.queries.chess_game_query import ChessGameQuery
from ...infrastructure.mappers.dto_mapper import DtoMapper
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository


class ChessGameQueryHandler(BaseQueryHandler[ChessGameQuery, ChessGameDto]):
    def __init__(self, repository: ChessGameRepository):
        self.repository = repository

    async def handle(self, request: ChessGameQuery) -> ChessGameDto:
        game = await self.repository.find(request.game_id.value)

        return DtoMapper.map_game(game)