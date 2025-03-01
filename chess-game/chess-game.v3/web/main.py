from contextlib import asynccontextmanager

from diator.container.rodi import RodiContainer
from diator.events import EventMap, EventEmitter
from diator.mediator import Mediator
from diator.middlewares import MiddlewareChain
from diator.requests import RequestMap

from rodi import Container

from core.application.handlers.game_started_handler import GameStartedEventHandler
from core.application.handlers.create_game_handler import CreateGameCommandHandler
from core.domain.commands.create_game import CreateGameCommand
from core.domain.events.game_started import GameStartedEvent
from fastapi import FastAPI

from core.infrastructure.config.config import initiate_database
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository
from web.api.main import api_router

@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    await initiate_database()

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

# to run - execute the command below
# fastapi dev main.py