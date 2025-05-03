import json
import traceback
from contextlib import asynccontextmanager
from beanie import PydanticObjectId
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState
from core.domain.chessboard.position import Position
from core.domain.events.piece_moved import PieceMoved
from core.domain.pieces.piece_factory import PieceFactory
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side
from core.infrastructure.config.config import initiate_database
from core.infrastructure.mediator.mediator import build_mediator
from web.api.main import api_router

@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    await initiate_database()

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # http://restack.io/p/fastapi-answer-websocket-kafka
    # https://adarsharegmi121.medium.com/building-real-time-applications-with-fastapi-and-apache-kafka-83f2c34b165d

    mediator = build_mediator()

    while True:
        # ToDo: get Event from Queue

        if websocket.application_state == WebSocketState.CONNECTED and websocket.client_state == WebSocketState.CONNECTED:
            json_string: str = await websocket.receive_text()
            try:
                serialized_data = json.loads(json_string)

                print(serialized_data)
                #{'game_id': '2f2c4f12-e536-4bb5-bc3a-d3049d9baf9f',
                # 'piece': {'_id': '112d2c5e-e43b-4e0d-83a1-c3291e0a9146', '_side': {'_value': 'W'}, '_type': 'P'},
                # 'from': 'e2', 'to': 'e4'}

                side = Side.black()
                if serialized_data['piece']['_side']['_value'] == 'W':
                    side = Side.white()

                piece_id = PieceId(serialized_data['piece']['_id'])
                game_id = PydanticObjectId(serialized_data['game_id'])

                piece_moved = PieceMoved(
                    game_id=ChessGameId(game_id),
                    piece=PieceFactory.create(piece_id, side, serialized_data['piece']['_type']),
                    from_=Position.parse(serialized_data['from']),
                    to=Position.parse(serialized_data['to']))

                await mediator.send(piece_moved)

                await websocket.send_json(json_string)
            except Exception:
                print('Could not deserialize json message via SignalR' + traceback.format_exc())

# to run - execute the command below
# fastapi dev main.py