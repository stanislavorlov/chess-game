import json
import traceback
from contextlib import asynccontextmanager
from typing import Annotated
from beanie import PydanticObjectId, init_beanie
from fastapi import FastAPI, WebSocket
from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from ..application.commands.move_piece_command import MovePieceCommand
from ..domain.chessboard.position import Position
from ..domain.pieces.piece_factory import PieceFactory
from ..domain.value_objects.game_id import ChessGameId
from ..domain.value_objects.piece_id import PieceId
from ..domain.value_objects.side import Side
from ..infrastructure import models
from ..infrastructure.config.config import Settings
from ..infrastructure.mediator.container import get_mediator, get_connection_manager
from ..infrastructure.mediator.mediator import Mediator
from ..interface.api.routes import game_api, move_api, piece_api
from ..interface.api.websockets.managers import BaseConnectionManager, ConnectionManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(Settings().MONGO_HOST)
    await init_beanie(
        database=client.get_database(Settings().MONGO_DB),
        document_models=models.__all__
    )

    yield

    # shutdown code goes here:
    client.close()


app = FastAPI(lifespan=lifespan, debug=True)

app.include_router(game_api.router)
app.include_router(move_api.router)
app.include_router(piece_api.router)

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(
        game_id: str,
        websocket: WebSocket,
        connection_manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
        mediator: Annotated[Mediator, Depends(get_mediator)]
):

    # ToDo: store connection in Redis instead of memory
    # connection_id = f"instance_id:{id(websocket)}"
    # redis_client.set(f"ws_connection:{user_id}", connection_id)
    # return redis_client.get(f"ws_connection:{user_id}")




    #connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    #mediator: Mediator = container.resolve(Mediator)

    # await websocket.accept()

    # ToDo: inject connection_manager into MovePieceCommandHandler
    await connection_manager.accept_connection(websocket=websocket, key=game_id)

    #try:
    while True:
        websocket_message: str = await websocket.receive_text()

        serialized_data = json.loads(websocket_message)
        side = Side.black()
        if serialized_data['piece']['_side']['_value'] == 'W':
            side = Side.white()

        piece_id = PieceId(serialized_data['piece']['_id'])
        game_id = PydanticObjectId(serialized_data['game_id'])

        piece_moved = MovePieceCommand(
            game_id=ChessGameId(game_id),
            piece=PieceFactory.create(piece_id, side, serialized_data['piece']['_type']),
            from_=Position.parse(serialized_data['from']),
            to=Position.parse(serialized_data['to']))

        await mediator.handle_command(piece_moved)

    #except WebSocketDisconnect:
    #    await connection_manager.remove_connection(websocket=websocket, key=game_id)
    #except:
    #    await websocket.send_json(data={"error": 'could not handle command'})
    #    await websocket.close()
