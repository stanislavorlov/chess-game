import asyncio

from diator.container.rodi import RodiContainer
from diator.events import (
    EventEmitter,
    EventMap,
)
from diator.mediator import Mediator
from diator.middlewares import MiddlewareChain
from diator.requests import RequestMap
from rodi import Container

from core.application.handlers.game_started_handler import GameStartedEventHandler
from core.application.handlers.start_game_handler import StartGameCommandHandler
from core.domain.commands.start_game import StartGameCommand
from core.domain.events.game_started import GameStartedEvent
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository

def setup_di() -> RodiContainer:
    container = Container()
    container.register(StartGameCommandHandler)
    container.register(GameStartedEventHandler)

    container.register(ChessGameRepository)

    rodi_container = RodiContainer()
    rodi_container.attach_external_container(container)

    return rodi_container

async def main() -> None:
    container = setup_di()

    event_map = EventMap()
    event_map.bind(GameStartedEvent, GameStartedEventHandler)

    middleware_chain = MiddlewareChain()

    request_map = RequestMap()
    request_map.bind(StartGameCommand, StartGameCommandHandler)

    event_emitter = EventEmitter(
        event_map=event_map, container=container, message_broker=None
    )

    mediator = Mediator(
        request_map=request_map,
        event_emitter=event_emitter,
        container=container,
        middleware_chain=middleware_chain,
    )

    await mediator.send(StartGameCommand())

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