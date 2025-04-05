import traceback
import uuid

from fastapi import APIRouter, WebSocket

from core.application.commands.create_game_command import CreateGameCommand
from core.application.queries.chess_game_query import ChessGameQuery
from core.domain.chessboard.board import Board
from core.domain.value_objects.game_format import GameFormat
from core.domain.value_objects.game_id import ChessGameId
from core.infrastructure.mediator.mediator import build_mediator
from web.api.models.create_board import CreateBoard

router = APIRouter(prefix="/api/game")

@router.post("/create_board/")
async def create_board(model: CreateBoard):
    mediator = build_mediator()

    try:
        game_id = ChessGameId.generate_id()
        game_format_obj = GameFormat.parse_string(model.game_format, model.time, model.additional)
        await mediator.send(CreateGameCommand(game_id=game_id, game_format=game_format_obj, name=model.name))

        query_result = await mediator.send(ChessGameQuery(game_id=game_id))

        return {
            "status": 200,
            "data": query_result
        }
    except Exception as e:
        print(e)
        print(traceback.format_exc())

        return {
            "status": 400
        }

@router.get("/board/{game_id}")
async def get_board(game_id: uuid.UUID):
    mediator = build_mediator()

    try:
        game_id = ChessGameId(game_id)

        query_result = await mediator.send(ChessGameQuery(game_id=game_id))

        return {
            "status": 200,
            "data": query_result
        }
    except Exception as e:
        print(e)
        print(traceback.format_exc())

        return {
            "status": 400
        }

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_json()

        await websocket.send_json(data)