import datetime
from chessapp.application.commands.create_game_command import CreateGameCommand
from chessapp.application.handlers.base_command_handler import BaseCommandHandler
from chessapp.domain.game.chess_game import ChessGame
from chessapp.domain.players.player_id import PlayerId
from chessapp.domain.players.players import Players
from chessapp.domain.value_objects.game_information import GameInformation
from chessapp.infrastructure.repositories.chess_game_repository import ChessGameRepository


class CreateGameCommandHandler(BaseCommandHandler[CreateGameCommand, None]):
    repository: ChessGameRepository

    async def handle(self, request: CreateGameCommand) -> None:
        game_info = GameInformation(request.game_format, datetime.datetime.now(), request.name)

        chess_game = ChessGame.create(request.game_id, game_info, Players(PlayerId(''), PlayerId('')))
        domain_events = chess_game.domain_events

        await self.repository.create(chess_game)