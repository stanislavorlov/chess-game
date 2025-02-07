import logging
import random

from diator.requests import RequestHandler
from core.domain.commands.start_game import StartGameCommand
from core.domain.game.chess_game_factory import ChessGameFactory
from core.domain.game.game_format import GameFormat
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.side import Side
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class StartGameCommandHandler(RequestHandler[StartGameCommand, None]):

    def __init__(self, repo: ChessGameRepository):
        self._chess_game_repo = repo
        self._events = []

    @property
    def events(self) -> list:
        return self._events

    async def handle(self, request: StartGameCommand) -> None:
        print('StartGameCommandHandler handle StartGameCommand')

        formats = [GameFormat.rapid(), GameFormat.blitz(), GameFormat.bullet()]
        format_: GameFormat = random.choice(formats)

        players = Players(PlayerId.of(Side.white()), PlayerId.of(Side.black()))

        game = ChessGameFactory.start_new(players, format_)
        game.start()

        self._chess_game_repo.save(game)

        self._events.extend(game.domain_events)