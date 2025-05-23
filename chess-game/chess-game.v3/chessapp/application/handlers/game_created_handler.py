from diator.events import EventHandler
from chessapp.domain.events.game_created import GameCreated
from chessapp.infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameCreatedEventHandler(EventHandler[GameCreated]):

    def __init__(self, repo: ChessGameRepository):
        self._chess_game_repo = repo
        self._events = []

    @property
    def events(self) -> list:
        return self._events

    async def handle(self, event: GameCreated) -> None:
        print('GameCreatedHandler handle GameCreated')
        chess_game = await self._chess_game_repo.find(event.game_id.value)

        # ToDo: player lookup logic & validation
        chess_game.start()

        await self._chess_game_repo.save(chess_game)