from diator.events import EventHandler
from core.domain.events.game_created import GameCreated
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameCreatedHandler(EventHandler[GameCreated]):

    def __init__(self, repo: ChessGameRepository):
        self._chess_game_repo = repo
        self._events = []

    @property
    def events(self) -> list:
        return self._events

    async def handle(self, event: GameCreated) -> None:
        print('GameCreatedHandler handle GameCreated')
        chess_game = await self._chess_game_repo.find_by_id(event.game_id)

        chess_game.start()