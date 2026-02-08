from collections import defaultdict
from functools import lru_cache

#from diator.container.rodi import RodiContainer
# from diator.events import EventMap, EventEmitter
# from diator.mediator import Mediator
# from diator.middlewares import MiddlewareChain
# from diator.requests import RequestMap
#from rodi import Container, ServiceLifeStyle
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
from punq import (
    Container,
    Scope,
)

def setup_mediator() -> Mediator:
    mediator: Mediator = Mediator()
    container: Container = setup_container()

    mediator.register_command(CreateGameCommand, [container.resolve(CreateGameCommandHandler)])
    mediator.register_command(MovePieceCommand, [container.resolve(MovePieceHandler)])
    mediator.register_query(ChessGameQuery, [container.resolve(ChessGameQueryHandler)])
    mediator.register_event(GameCreated, [container.resolve(GameCreatedEventHandler)])
    mediator.register_event(GameStarted, [container.resolve(GameStartedEventHandler)])

    return mediator

def setup_container() -> Container:
    container: Container = Container()
    container.register(ChessGameRepository, scope=Scope.transient)
    container.register(MovementService)
    container.register(GameStartedEventHandler)
    container.register(CreateGameCommandHandler)
    container.register(ChessGameQueryHandler)
    container.register(MovePieceHandler)
    container.register(GameCreatedEventHandler)

    container.register(
        BaseConnectionManager,
        instance=ConnectionManager(),
        scope=Scope.singleton,
    )

    return container

@lru_cache(1)
def init_container() -> Container:
    return __init_container()

def __init_container() -> Container:
    container = Container()
    container.register(ChessGameRepository)
    container.register(MovementService)
    container.register(GameStartedEventHandler)
    container.register(CreateGameCommandHandler)
    container.register(ChessGameQueryHandler)
    container.register(MovePieceHandler)
    container.register(GameCreatedEventHandler)

    #container.register(Mediator, factory=)
    #container.register_factory(factory=build_mediator, return_type=Mediator, life_style=ServiceLifeStyle.SINGLETON)

    # container.register(
    #     BaseConnectionManager,
    #     instance=ConnectionManager(),
    # )

    #container.add_singleton(ConnectionManager, ConnectionManager)

    # https://github.com/AlexanderLukash/fastapi-websocket-chat-kafka/blob/main/app/logic/init.py#L142
    #container.add_singleton(BaseConnectionManager, ConnectionManager)

    container.register(
        BaseConnectionManager,
        instance=ConnectionManager(),
        scope=Scope.singleton,
    )

    return container

    # def build_request_map():
    #     request_map = RequestMap()
    #     request_map.bind(CreateGameCommand, CreateGameCommandHandler)
    #     request_map.bind(ChessGameQuery, ChessGameQueryHandler)
    #     request_map.bind(MovePieceCommand, MovePieceHandler)
    #
    #     return request_map

    # def build_mediator() -> Mediator:
    #     event_map = EventMap()
    #     event_map.bind(GameStarted, GameStartedEventHandler)
    #     event_map.bind(GameCreated, GameCreatedEventHandler)
    #
    #     middleware_chain = MiddlewareChain()
    #
    #     event_emitter = EventEmitter(
    #         event_map=event_map, container=container
    #     )
    #
    #     mediator_ = Mediator(
    #         request_map=build_request_map(),
    #         event_emitter=event_emitter,
    #         container=container,
    #         middleware_chain=middleware_chain,
    #     )
    #
    #     return mediator_
    #
    # # Do I need a Mediator if Kafka in place ???
    # # or copy and create a local copy
    #
    # mediator = build_mediator()
    #
    # container.register(
    #     'mediator',
    #     instance=mediator,
    #     scope=Scope.singleton)
    #
    # return container