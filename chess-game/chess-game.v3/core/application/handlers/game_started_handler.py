import logging

from diator.events import EventHandler

from core.domain.events.game_started import GameStartedEvent
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameStartedEventHandler(EventHandler[GameStartedEvent]):

    def __init__(self, repo: ChessGameRepository):
        self._chess_game_repo = repo

    async def handle(self, event: GameStartedEvent) -> None:
        print('GameStartedEventHandler handle GameStartedEvent')

        game = self._chess_game_repo.get(event.game_id)
        print(game)