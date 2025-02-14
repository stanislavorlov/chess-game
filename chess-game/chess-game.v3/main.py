from contextlib import asynccontextmanager
from functools import lru_cache

import pymongo
from diator.container.rodi import RodiContainer
from diator.events import EventMap, EventEmitter
from diator.mediator import Mediator
from diator.middlewares import MiddlewareChain
from diator.requests import RequestMap
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from rodi import Container

from core.application.handlers.game_started_handler import GameStartedEventHandler
from core.application.handlers.start_game_handler import StartGameCommandHandler
from core.domain.commands.start_game import StartGameCommand
from core.domain.events.game_started import GameStartedEvent
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository
from fastapi import FastAPI
from web.api.main import api_router

import config

mediator: Mediator

@asynccontextmanager
async def lifespan(fast_api: FastAPI):
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

    global mediator
    mediator = Mediator(
        request_map=request_map,
        event_emitter=event_emitter,
        container=rodi_container,
        middleware_chain=middleware_chain,
    )

    yield

app = FastAPI(lifespan=lifespan)
#router = APIRouter(tags=["stacks"])

@lru_cache
def get_settings():
    return config.Settings()

#uri = "mongodb+srv://stasorlov21:1ibAsmJf2SUq95Ba@cluster0.cchn0.mongodb.net/?retryWrites=true&w=majority"
print(get_settings().MONGO_HOST)
#print(config.Settings.MONGO_HOST, config.Settings.MONGO_DB)
#app.mongo_client = MongoClient(config.Settings.MONGO_HOST,tls=True,tlsAllowInvalidCertificates=True)
#app.mongodb = app.mongo_client[config.Settings.MONGO_DB]

app.include_router(api_router)

# @app.get("/")
# async def read_root():
#     await mediator.send(StartGameCommand())
#
#     return {"Hello": "World"}
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# to run - execute the command below
# fastapi dev main.py