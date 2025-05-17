import json
import traceback
from contextlib import asynccontextmanager
from beanie import PydanticObjectId, init_beanie
from diator.mediator import Mediator
from fastapi import FastAPI
from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from rodi import Container
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect
from chessapp.application.commands.move_piece_command import MovePieceCommand
from chessapp.domain.chessboard.position import Position
from chessapp.domain.pieces.piece_factory import PieceFactory
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side
from chessapp.infrastructure import models
from chessapp.infrastructure.config.config import Settings
from chessapp.infrastructure.mediator.mediator import build_mediator, init_container
from chessapp.interface.api.main import api_router
from chessapp.interface.api.websockets.managers import BaseConnectionManager, ConnectionManager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    client = AsyncIOMotorClient(Settings().MONGO_HOST)
    await init_beanie(
        database=client.get_database(Settings().MONGO_DB),
        document_models=models.__all__
    )

    yield

    # shutdown code goes here:
    client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

# ToDo: @app.websocket("/ws/{game_id}")
# async def websocket_endpoint(game_id: str, websocket: WebSocket):

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(
        game_id: str,
        websocket: WebSocket,
        container: Container = Depends(init_container)
):
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    mediator: Mediator = container.resolve(Mediator)

    await websocket.accept()

    # ToDo: inject connection_manager into MovePieceCommandHandler
    await connection_manager.accept_connection(websocket=websocket, key=game_id)

    try:
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

            await mediator.send(piece_moved)

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket=websocket, key=game_id)
    except:
        await websocket.send_json(data={"error": 'could not handle command'})
        await websocket.close()

    ################################################

    # mediator = build_mediator()
    #
    # while True:
    #     # ToDo: get Event from Queue
    #
    #     if websocket.application_state == WebSocketState.CONNECTED and websocket.client_state == WebSocketState.CONNECTED:
    #         json_string: str = await websocket.receive_text()
    #         try:
    #             serialized_data = json.loads(json_string)
    #
    #             side = Side.black()
    #             if serialized_data['piece']['_side']['_value'] == 'W':
    #                 side = Side.white()
    #
    #             piece_id = PieceId(serialized_data['piece']['_id'])
    #             game_id = PydanticObjectId(serialized_data['game_id'])
    #
    #             piece_moved = MovePieceCommand(
    #                 game_id=ChessGameId(game_id),
    #                 piece=PieceFactory.create(piece_id, side, serialized_data['piece']['_type']),
    #                 from_=Position.parse(serialized_data['from']),
    #                 to=Position.parse(serialized_data['to']))
    #
    #             await mediator.send(piece_moved)
    #
    #             await websocket.send_json(json_string)
    #         except Exception:
    #             print('Could not deserialize json message via SignalR' + traceback.format_exc())

# to run - execute the command below
# fastapi dev main.py