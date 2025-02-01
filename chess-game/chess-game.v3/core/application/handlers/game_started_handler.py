from diator.requests import RequestHandler

from core.domain.events.game_started import GameStartedCommand
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameStartedHandler(RequestHandler[GameStartedCommand, None]):

    def __init__(self, repo: ChessGameRepository):
        self._chess_game_repo = repo

    async def handle(self, request: GameStartedCommand) -> None:
        print('Game started')