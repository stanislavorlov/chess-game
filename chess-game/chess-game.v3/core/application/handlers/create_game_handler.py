import datetime

from diator.requests import RequestHandler
from core.application.commands.create_game_command import CreateGameCommand
from core.domain.game.chess_game import ChessGame
from core.domain.game.game_settings import GameSettings
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_information import GameInformation
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class CreateGameCommandHandler(RequestHandler[CreateGameCommand, None]):

    def __init__(self, repo: ChessGameRepository):
        self._repository = repo
        self._events = []

    @property
    def events(self) -> list:
        return self._events

    async def handle(self, request: CreateGameCommand) -> None:
        game_settings = GameSettings(request.game_format)
        game_info = GameInformation(0, datetime.datetime.now(), 'Chess Game 1')

        chess_game = ChessGame.create(request.game_id, game_settings, game_info, Players(PlayerId(''), PlayerId('')))

        chess_game = await self._repository.create(chess_game)

        self._events.extend(chess_game.domain_events)