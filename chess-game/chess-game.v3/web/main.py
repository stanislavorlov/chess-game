import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState

from core.domain.movements.movement import Movement
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
        if websocket.application_state == WebSocketState.CONNECTED and websocket.client_state == WebSocketState.CONNECTED:
            json_string: str = await websocket.receive_text()
            try:
                serialized_data = json.loads(json_string)

                print(serialized_data)

                # movement = Movement()

                await websocket.send_json(json_string)
            except:
                print('Could not deserialize json message via SignalR' + json_string)

# to run - execute the command below
# fastapi dev main.py