import logging
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
from ...domain.events.game_created import GameCreated
from ...domain.events.game_started import GameStarted
from ...infrastructure.mediator.mediator import Mediator
from ...infrastructure.config.config import Settings
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository
from ...infrastructure.services.redis_service import RedisService
from ...infrastructure.services.kafka_service import KafkaProducerService
from ...interface.api.websockets.managers import BaseConnectionManager, ConnectionManager

@lru_cache(1)
def get_settings() -> Settings:
    return Settings()

@lru_cache(1)
def get_redis_service(settings: Annotated[Settings, Depends(get_settings)]) -> RedisService:
    return RedisService(settings)

@lru_cache(1)
def get_kafka_service(settings: Annotated[Settings, Depends(get_settings)]) -> KafkaProducerService:
    return KafkaProducerService(settings)

@lru_cache(1)
def get_connection_manager() -> ConnectionManager:
    return ConnectionManager()

def get_repository() -> ChessGameRepository:
    return ChessGameRepository()

@lru_cache(1)
def get_logger() -> logging.Logger:
    return logging.getLogger("chessapp")

def get_mediator(
    repo: Annotated[ChessGameRepository, Depends(get_repository)],
    connection_manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
    logger: Annotated[logging.Logger, Depends(get_logger)]
) -> Mediator:
    mediator = Mediator()
    # Reset mediator for registration to avoid duplicate handlers if re-called (though Depends caches by default)
    mediator._reset()

    mediator.register_command(CreateGameCommand, [CreateGameCommandHandler(repo)])
    mediator.register_command(MovePieceCommand, [MovePieceHandler(repo, connection_manager, logger)])
    mediator.register_query(ChessGameQuery, [ChessGameQueryHandler(repo)])
    mediator.register_event(GameCreated, [GameCreatedEventHandler(repo)])
    mediator.register_event(GameStarted, [GameStartedEventHandler(repo)])

    return mediator