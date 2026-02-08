from ...application.handlers.base_event_handler import BaseEventHandler
from ...domain.events.game_started import GameStarted
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameStartedEventHandler(BaseEventHandler[GameStarted, None]):
    repo: ChessGameRepository

    async def handle(self, event: GameStarted) -> None:
        print('GameStartedEventHandler handle GameStartedEvent')

        game = self.repo.find(event.game_id.value)
        print(game)