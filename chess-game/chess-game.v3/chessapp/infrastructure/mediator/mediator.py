from collections import defaultdict

from diator.container.rodi import RodiContainer
from diator.events import EventMap, EventEmitter
from diator.mediator import Mediator
from diator.middlewares import MiddlewareChain
from diator.requests import RequestMap
from rodi import Container, ServiceLifeStyle
from chessapp.application.commands.move_piece_command import MovePieceCommand
from chessapp.application.handlers.game_created_handler import GameCreatedEventHandler
from chessapp.application.handlers.game_query_handler import ChessGameQueryHandler
from chessapp.application.handlers.game_started_handler import GameStartedEventHandler
from chessapp.application.handlers.create_game_handler import CreateGameCommandHandler
from chessapp.application.commands.create_game_command import CreateGameCommand
from chessapp.application.handlers.move_piece_handler import MovePieceHandler
from chessapp.application.queries.chess_game_query import ChessGameQuery
from chessapp.application.services.movement_service import MovementService
from chessapp.domain.events.game_created import GameCreated
from chessapp.domain.events.game_started import GameStarted
from chessapp.infrastructure.repositories.chess_game_repository import ChessGameRepository
from chessapp.interface.api.websockets.managers import BaseConnectionManager, ConnectionManager


def init_container() -> Container:
    container = Container()
    container.register(ChessGameRepository)
    container.register(MovementService)
    container.register(GameStartedEventHandler)
    container.register(CreateGameCommandHandler)
    container.register(ChessGameQueryHandler)
    container.register(MovePieceHandler)
    container.register(GameCreatedEventHandler)

    #container.register(Mediator, factory=)
    container.register_factory(factory=build_mediator, return_type=Mediator, life_style=ServiceLifeStyle.SINGLETON)

    # container.register(
    #     BaseConnectionManager,
    #     instance=ConnectionManager(),
    # )

    #container.add_singleton(ConnectionManager, ConnectionManager)
    container.add_singleton(BaseConnectionManager)

    return container

def build_mediator() -> Mediator:
    container = init_container()

    rodi_container = RodiContainer()
    rodi_container.attach_external_container(container)

    event_map = EventMap()
    event_map.bind(GameStarted, GameStartedEventHandler)
    event_map.bind(GameCreated, GameCreatedEventHandler)

    middleware_chain = MiddlewareChain()

    request_map = RequestMap()
    request_map.bind(CreateGameCommand, CreateGameCommandHandler)
    request_map.bind(ChessGameQuery, ChessGameQueryHandler)
    request_map.bind(MovePieceCommand, MovePieceHandler)

    event_emitter = EventEmitter(
        event_map=event_map, container=rodi_container, message_broker=None
    )

    mediator = Mediator(
        request_map=request_map,
        event_emitter=event_emitter,
        container=rodi_container,
        middleware_chain=middleware_chain,
    )

    return mediator