import logging
import random

from diator.requests import RequestHandler
from core.domain.commands.start_game import StartGameCommand
from core.domain.game.chess_game import ChessGame
from core.domain.game.chess_game_factory import ChessGameFactory
from core.domain.game.game_format import GameFormat
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.side import Side
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class StartGameCommandHandler(RequestHandler[StartGameCommand, None]):

    def __init__(self, repo: ChessGameRepository):
        self._repository = repo
        self._events = []

    @property
    def events(self) -> list:
        return self._events

    async def handle(self, request: StartGameCommand) -> None:
        print('StartGameCommandHandler handle StartGameCommand')

        chess_game = ChessGameFactory.start_new(request.format_)
        game_created = await self._repository.create(chess_game)

        self._events.extend(chess_game.domain_events)

        return chess_game