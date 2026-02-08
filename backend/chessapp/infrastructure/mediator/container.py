from functools import lru_cache
from typing import Annotated
from fastapi import Depends

from ...application.commands.move_piece_command import MovePieceCommand
from ...application.handlers.game_created_handler import GameCreatedEventHandler
from ...application.handlers.game_query_handler import ChessGameQueryHandler
from ...application.handlers.game_started_handler import GameStartedEventHandler
from ...application.handlers.create_game_handler import CreateGameCommandHandler
from ...application.commands.create_game_command import CreateGameCommand
from ...application.handlers.move_piece_handler import MovePieceHandler
from ...application.queries.chess_game_query import ChessGameQuery
from ...application.services.movement_service import MovementService
from ...domain.events.game_created import GameCreated
from ...domain.events.game_started import GameStarted
from ...infrastructure.mediator.mediator import Mediator
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository
from ...interface.api.websockets.managers import BaseConnectionManager, ConnectionManager

@lru_cache(1)
def get_connection_manager() -> ConnectionManager:
    return ConnectionManager()

def get_repository() -> ChessGameRepository:
    return ChessGameRepository()

def get_movement_service(repo: Annotated[ChessGameRepository, Depends(get_repository)]) -> MovementService:
    return MovementService(repo)

def get_mediator(
    repo: Annotated[ChessGameRepository, Depends(get_repository)],
    movement_service: Annotated[MovementService, Depends(get_movement_service)],
    connection_manager: Annotated[ConnectionManager, Depends(get_connection_manager)]
) -> Mediator:
    mediator = Mediator()
    # Reset mediator for registration to avoid duplicate handlers if re-called (though Depends caches by default)
    mediator._reset()

    mediator.register_command(CreateGameCommand, [CreateGameCommandHandler(repo)])
    mediator.register_command(MovePieceCommand, [MovePieceHandler(movement_service, connection_manager)])
    mediator.register_query(ChessGameQuery, [ChessGameQueryHandler(repo)])
    mediator.register_event(GameCreated, [GameCreatedEventHandler(repo)])
    mediator.register_event(GameStarted, [GameStartedEventHandler(repo)])

    return mediator