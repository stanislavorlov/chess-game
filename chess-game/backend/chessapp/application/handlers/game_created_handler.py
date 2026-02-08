from ...application.handlers.base_event_handler import BaseEventHandler
from ...domain.events.game_created import GameCreated
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository


class GameCreatedEventHandler(BaseEventHandler[GameCreated, None]):
    repository: ChessGameRepository

    async def handle(self, event: GameCreated) -> None:
        print('GameCreatedHandler handle GameCreated')
        chess_game = await self.repository.find(event.game_id.value)

        # ToDo: player lookup logic & validation
        chess_game.start()

        await self.repository.save(chess_game)