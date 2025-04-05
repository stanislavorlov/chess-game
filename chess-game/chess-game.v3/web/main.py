from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.websockets import WebSocket
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

    mediator = build_mediator()

    while True:
        data = await websocket.receive_json()

        print(data)

        await websocket.send_json(data)

# to run - execute the command below
# fastapi dev main.py