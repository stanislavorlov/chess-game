from ...application.handlers.base_event_handler import BaseEventHandler
from ...domain.events.game_started import GameStarted
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameStartedEventHandler(BaseEventHandler[GameStarted, None]):
    def __init__(self, repo: ChessGameRepository):
        self.repo = repo

    async def handle(self, event: GameStarted) -> None:
        print('GameStartedEventHandler handle GameStartedEvent')

        game = await self.repo.find(event.game_id.value)
        if game:
            await self.repo.save(game)
        print(game)