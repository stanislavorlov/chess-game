import logging
import random

from diator.requests import RequestHandler
from core.domain.commands.create_game import CreateGameCommand
from core.domain.game.chess_game import ChessGame
from core.domain.game.game_format import GameFormat
from core.domain.game.game_settings import GameSettings
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.side import Side
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class CreateGameCommandHandler(RequestHandler[CreateGameCommand, None]):

    def __init__(self, repo: ChessGameRepository):
        self._repository = repo
        self._events = []

    @property
    def events(self) -> list:
        return self._events

    async def handle(self, request: CreateGameCommand) -> None:
        print('StartGameCommandHandler handle StartGameCommand')

        chess_game = ChessGame.create(GameSettings(request.format_), Players(PlayerId(''), PlayerId('')))
        await self._repository.create(chess_game)

        self._events.extend(chess_game.domain_events)

        return chess_game