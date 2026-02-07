from chessapp.application.handlers.base_event_handler import BaseEventHandler
from chessapp.domain.events.game_started import GameStarted
from chessapp.infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameStartedEventHandler(BaseEventHandler[GameStarted, None]):
    repo: ChessGameRepository

    async def handle(self, event: GameStarted) -> None:
        print('GameStartedEventHandler handle GameStartedEvent')

        game = self.repo.find(event.game_id.value)
        print(game)