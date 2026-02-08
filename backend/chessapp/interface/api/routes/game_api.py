import traceback
from typing import Dict, Any, Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ....application.commands.create_game_command import CreateGameCommand
from ....application.queries.chess_game_query import ChessGameQuery
from ....domain.value_objects.game_format import GameFormat
from ....domain.value_objects.game_id import ChessGameId
from ....infrastructure.mediator.container import get_mediator
from ....infrastructure.mediator.mediator import Mediator
from ....interface.api.models.create_board import CreateBoard

router = APIRouter(prefix="/api/game")

class GameResponse(BaseModel):
    status: int
    data: Any = None


@router.post("/create_board/")
async def create_board(mediator: Annotated[Mediator, Depends(get_mediator)],
                       model: CreateBoard):
    try:
        game_id = ChessGameId.generate_id()
        game_format_obj = GameFormat.parse_string(model.game_format, model.time, model.additional)
        await mediator.handle_command(CreateGameCommand(game_id=game_id, game_format=game_format_obj, name=model.name))

        query_result = await mediator.handle_query(ChessGameQuery(game_id=game_id))

        return {
            "status": 200,
            "data": GameResponse(status=200, data=next(query_result))
        }
    except Exception as e:
        print(e)
        print(traceback.format_exc())

        return {
            "status": 400
        }

@router.get("/board/{game_id}")
async def get_board(mediator: Annotated[Mediator, Depends(get_mediator)], game_id: str):
    try:
        game_id = ChessGameId(PydanticObjectId(game_id))

        print(mediator)

        query_result = await mediator.handle_query(ChessGameQuery(game_id=game_id))

        return GameResponse(status=200, data=next(iter(query_result)))
    except Exception as e:
        print(e)
        print(traceback.format_exc())

        return {
            "status": 400
        }