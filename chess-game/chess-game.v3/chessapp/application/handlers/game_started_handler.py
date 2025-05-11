from diator.events import EventHandler
from chessapp.domain.events.game_started import GameStarted
from chessapp.infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameStartedEventHandler(EventHandler[GameStarted]):

    def __init__(self, repo: ChessGameRepository):
        self._chess_game_repo = repo

    async def handle(self, event: GameStarted) -> None:
        print('GameStartedEventHandler handle GameStartedEvent')

        game = self._chess_game_repo.find(event.game_id.value)
        print(game)