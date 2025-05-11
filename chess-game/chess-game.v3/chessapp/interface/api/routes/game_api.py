import traceback
from beanie import PydanticObjectId
from fastapi import APIRouter
from chessapp.application.commands.create_game_command import CreateGameCommand
from chessapp.application.queries.chess_game_query import ChessGameQuery
from chessapp.domain.value_objects.game_format import GameFormat
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.infrastructure.mediator.mediator import build_mediator
from chessapp.interface.api.models.create_board import CreateBoard

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
async def get_board(game_id: str):
    mediator = build_mediator()

    try:
        game_id = ChessGameId(PydanticObjectId(game_id))

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