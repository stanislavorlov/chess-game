import random

# from di import bind_by_type, Container
# from di.dependent import Dependent
# from diator.container.di import DIContainer
# import asyncio
# from dataclasses import dataclass, field
# from diator.events import Event, EventMap
# from diator.mediator import Mediator
# from diator.middlewares import MiddlewareChain
# from diator.requests import Request, RequestHandler
# from diator.requests import Request, RequestMap
# from diator.events import Event, EventEmitter
#
# from core.application.handlers.movement_completed_handler import MovementCompletedHandler
# from core.application.handlers.movement_started_handler import MovementStartedHandler
# from core.application.handlers.piece_selected_handler import PieceSelectedHandler
# from core.application.handlers.player_side_selected_handler import PlayerSideSelectedHandler
# from core.domain.events.game_started import GameStartedCommand
# from core.domain.events.movement_completed import MovementCompleted
# from core.domain.events.movement_started import MovementStarted
# from core.domain.events.piece_selected import PieceSelected
# from core.domain.events.player_side_selected import PlayerSideSelected
# from core.domain.game.game_state import GameState
# from core.domain.value_objects.side import Side
# from core.domain.game.chess_game import ChessGame
# from core.infrastructure.mediator import Mediator
# from core.interface.char_presenter import CharacterPresenter

import asyncio

from di import Container, bind_by_type
from di.dependent import Dependent

from diator.container.di import DIContainer
from diator.events import (
    DomainEvent,
    EventEmitter,
    EventHandler,
    EventMap,
    NotificationEvent,
)
from diator.mediator import Mediator
from diator.middlewares import MiddlewareChain
from diator.requests import Request, RequestHandler, RequestMap

from core.application.handlers.game_started_handler import GameStartedHandler
from core.application.handlers.player_side_selected_handler import PlayerSideSelectedHandler
from core.domain.events.game_started import GameStartedCommand
from core.domain.events.player_side_selected import PlayerSideSelected


# ToDo: move all this logic into ChessGame object
# ToDo: Store ChessGame into repo
# ToDo: no direct invocation between objects, only Events and handlers


def setup_di() -> DIContainer:
    external_container = Container()
    external_container.bind(
        bind_by_type(
            Dependent(PlayerSideSelectedHandler, scope= "request"),
            PlayerSideSelectedHandler
        )
    )

    container = DIContainer()
    container.attach_external_container(external_container)

    return container

async def main() -> None:
    container = setup_di()

    event_map = EventMap()
    #event_map.bind()

    middleware_chain = MiddlewareChain()

    request_map = RequestMap()
    request_map.bind(PlayerSideSelected, PlayerSideSelectedHandler)
    request_map.bind(GameStartedCommand, GameStartedHandler)

    event_emitter = EventEmitter(
        event_map=event_map, container=container, message_broker=None
    )

    mediator = Mediator(
        request_map=request_map,
        event_emitter=event_emitter,
        container=container,
        middleware_chain=middleware_chain,
    )

    await mediator.send(GameStartedCommand())

if __name__ == '__main__':
    asyncio.run(main())

#sides = [Side.white(), Side.black()]
#start_side: Side = random.choice(sides)
#print("Your game side:" + str(start_side))

# Once selected publish PlayerSideSelected event

#state = GameState()
#presenter = ImagePresenter()
#presenter = CharacterPresenter()

#mediator = Mediator()
#mediator.bind(MovementCompleted, MovementCompletedHandler)
#mediator.bind(MovementStarted, MovementStartedHandler)
#mediator.bind(PieceSelected, PieceSelectedHandler)
#mediator.bind(PlayerSideSelected, PlayerSideSelectedHandler)

#mediator.publish(PlayerSideSelected(start_side))

#game = ChessGame(state, presenter, specification)
#game.start(start_side)

# ToDo: publish game started event instead