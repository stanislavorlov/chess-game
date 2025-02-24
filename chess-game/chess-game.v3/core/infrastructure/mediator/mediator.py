from diator.container.rodi import RodiContainer
from diator.events import EventMap, EventEmitter
from diator.mediator import Mediator
from diator.middlewares import MiddlewareChain
from diator.requests import RequestMap
from rodi import Container

from core.application.handlers.game_started_handler import GameStartedEventHandler
from core.application.handlers.start_game_handler import StartGameCommandHandler
from core.domain.commands.start_game import StartGameCommand
from core.domain.events.game_started import GameStartedEvent
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


def build_mediator() -> Mediator:
    container = Container()
    container.register(ChessGameRepository)
    container.register(GameStartedEventHandler)
    container.register(StartGameCommandHandler)

    rodi_container = RodiContainer()
    rodi_container.attach_external_container(container)

    event_map = EventMap()
    event_map.bind(GameStartedEvent, GameStartedEventHandler)

    middleware_chain = MiddlewareChain()

    request_map = RequestMap()
    request_map.bind(StartGameCommand, StartGameCommandHandler)

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