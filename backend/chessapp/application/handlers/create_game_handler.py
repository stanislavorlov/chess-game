import datetime
from ...application.commands.create_game_command import CreateGameCommand
from ...application.dtos.chess_game_dto import ChessGameDto
from ...application.handlers.base_command_handler import BaseCommandHandler
from ...domain.game.chess_game import ChessGame
from ...domain.players.player_id import PlayerId
from ...domain.players.players import Players
from ...domain.value_objects.game_information import GameInformation
from ...infrastructure.mappers.dto_mapper import DtoMapper
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository


class CreateGameCommandHandler(BaseCommandHandler[CreateGameCommand, ChessGameDto]):
    def __init__(self, repository: ChessGameRepository):
        self.repository = repository

    async def handle(self, request: CreateGameCommand) -> ChessGameDto:
        game_info = GameInformation(request.game_format, datetime.datetime.now(), request.name)

        chess_game = ChessGame.create(request.game_id, game_info, Players(PlayerId(''), PlayerId('')))

        created_game = await self.repository.create(chess_game)

        return DtoMapper.map_game(created_game)