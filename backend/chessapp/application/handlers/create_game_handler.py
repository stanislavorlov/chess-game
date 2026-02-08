import datetime
from ...application.commands.create_game_command import CreateGameCommand
from ...application.handlers.base_command_handler import BaseCommandHandler
from ...domain.game.chess_game import ChessGame
from ...domain.players.player_id import PlayerId
from ...domain.players.players import Players
from ...domain.value_objects.game_information import GameInformation
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository


class CreateGameCommandHandler(BaseCommandHandler[CreateGameCommand, None]):
    def __init__(self, repository: ChessGameRepository):
        self.repository = repository

    async def handle(self, request: CreateGameCommand) -> None:
        game_info = GameInformation(request.game_format, datetime.datetime.now(), request.name)

        chess_game = ChessGame.create(request.game_id, game_info, Players(PlayerId(''), PlayerId('')))
        domain_events = chess_game.domain_events

        await self.repository.create(chess_game)