from diator.events import EventHandler

from core.domain.events.game_started import GameStartedEvent
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameStartedEventHandler(EventHandler[GameStartedEvent]):

    def __init__(self, repo: ChessGameRepository):
        self._chess_game_repo = repo

    async def handle(self, event: GameStartedEvent) -> None:
        print('game started handler')