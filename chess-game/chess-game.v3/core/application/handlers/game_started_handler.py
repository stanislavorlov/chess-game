import random

from diator.requests import RequestHandler

from core.domain.events.game_started import GameStartedCommand
from core.domain.game.chess_game_factory import ChessGameFactory
from core.domain.game.game_format import GameFormat
from core.domain.value_objects.side import Side
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameStartedHandler(RequestHandler[GameStartedCommand, None]):

    def __init__(self, repo: ChessGameRepository):
        self._chess_game_repo = repo

    async def handle(self, request: GameStartedCommand) -> None:
        sides = [Side.white(), Side.black()]
        start_side: Side = random.choice(sides)

        formats = [GameFormat.rapid(), GameFormat.blitz(), GameFormat.bullet()]
        format_: GameFormat = random.choice(formats)

        game = ChessGameFactory.start_new(start_side, format_)

        self._chess_game_repo.save(game)