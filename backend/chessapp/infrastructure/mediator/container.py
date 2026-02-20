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
from ...infrastructure.services.redis_service import RedisService
from ...infrastructure.services.kafka_service import KafkaService
from ...interface.api.websockets.managers import BaseConnectionManager, ConnectionManager

from ...domain.events.game_created import GameCreated
from ...domain.events.game_started import GameStarted
from ...domain.events.game_finished import GameFinished
from ...domain.events.game_start_failed import GameStartFailed
from ...domain.events.king_castled import KingCastled
from ...domain.events.king_checked import KingChecked
from ...domain.events.king_checkmated import KingCheckMated
from ...domain.events.pawn_promoted import PawnPromoted
from ...domain.events.piece_captured import PieceCaptured
from ...domain.events.piece_move_failed import PieceMoveFailed
from ...domain.events.piece_moved import PieceMoved
from ...application.handlers.redis_notification_handler import RedisNotificationHandler
from ...infrastructure.mediator.mediator import Mediator
from ...infrastructure.config.config import Settings
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository

@lru_cache(1)
def get_settings() -> Settings:
    return Settings()

@lru_cache(1)
def get_redis_service() -> RedisService:
    settings = get_settings()
    return RedisService(settings)

@lru_cache(1)
def get_kafka_service() -> KafkaService:
    settings = get_settings()
    return KafkaService(settings)

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
    redis_service: Annotated[RedisService, Depends(get_redis_service)],
    logger: Annotated[logging.Logger, Depends(get_logger)]
) -> Mediator:
    mediator = Mediator()
    # Reset mediator for registration to avoid duplicate handlers if re-called (though Depends caches by default)
    mediator.reset()

    # Handlers dependencies
    notification_handler = RedisNotificationHandler(redis_service)

    mediator.register_command(CreateGameCommand, [CreateGameCommandHandler(repo, mediator)])
    mediator.register_command(MovePieceCommand, [MovePieceHandler(repo, mediator, logger)])
    mediator.register_query(ChessGameQuery, [ChessGameQueryHandler(repo)])
    
    # Event Handlers
    mediator.register_event(GameCreated, [GameCreatedEventHandler(repo, mediator), notification_handler])
    
    # Register all events for Redis notification
    all_events = [
        GameCreated, GameStarted, GameFinished, GameStartFailed,
        KingCastled, KingChecked, KingCheckMated, PawnPromoted,
        PieceCaptured, PieceMoveFailed, PieceMoved
    ]
    for event_cls in all_events:
        if event_cls != GameCreated: 
             mediator.register_event(event_cls, [notification_handler])
             
    mediator.register_event(GameStarted, [GameStartedEventHandler(repo)])

    return mediator