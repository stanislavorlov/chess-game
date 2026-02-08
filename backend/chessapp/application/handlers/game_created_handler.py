from ...application.handlers.base_event_handler import BaseEventHandler
from ...domain.events.game_created import GameCreated
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository
from ...infrastructure.mediator.mediator import Mediator


class GameCreatedEventHandler(BaseEventHandler[GameCreated, None]):
    def __init__(self, repository: ChessGameRepository, mediator: Mediator):
        self.repository = repository
        self.mediator = mediator

    async def handle(self, event: GameCreated) -> None:
        print('GameCreatedHandler handle GameCreated')
        chess_game = await self.repository.find(event.game_id.value)

        # ToDo: player lookup logic & validation
        chess_game.start()

        await self.repository.save(chess_game)

        # Dispatch domain events collected in the aggregate (e.g. GameStarted)
        await self.mediator.dispatch_events(chess_game)