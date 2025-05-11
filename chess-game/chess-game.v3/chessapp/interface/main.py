import json
import traceback
from contextlib import asynccontextmanager
from beanie import PydanticObjectId
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState
from chessapp.domain.chessboard.position import Position
from chessapp.domain.events.piece_moved import PieceMoved
from chessapp.domain.pieces.piece_factory import PieceFactory
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side
from chessapp.infrastructure.config.config import initiate_database
from chessapp.infrastructure.mediator.mediator import build_mediator
from chessapp.interface.api.main import api_router


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