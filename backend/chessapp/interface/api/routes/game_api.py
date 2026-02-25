import traceback
import logging
from typing import Dict, Any, Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Response, HTTPException
from pydantic import BaseModel
from ....application.commands.create_game_command import CreateGameCommand
from ....application.queries.chess_game_query import ChessGameQuery
from ....domain.value_objects.game_format import GameFormat
from ....domain.value_objects.game_id import ChessGameId
from ....infrastructure.mediator.container import get_mediator
from ....infrastructure.mediator.mediator import Mediator
from ....interface.api.models.create_board import CreateBoard

router = APIRouter(prefix="/api/game")
logger = logging.getLogger("chessapp")


@router.post("/create_board/", response_model=Any)
async def create_board(mediator: Annotated[Mediator, Depends(get_mediator)],
                       model: CreateBoard):
    try:
        game_id = ChessGameId.generate_id()
        game_format_obj = GameFormat.parse_string(model.format, model.time, model.increment)
        command_result = await mediator.handle_command(CreateGameCommand(game_id=game_id, game_format=game_format_obj, name=model.name))

        logger.debug(f"CreateGameCommand result: {command_result}")

        return next(iter(command_result))
    except Exception as e:
        logger.error(f"Error creating board: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/board/{game_id}", response_model=Any)
async def get_board(mediator: Annotated[Mediator, Depends(get_mediator)], game_id: str):
    try:
        game_id = ChessGameId(PydanticObjectId(game_id))

        query_result = await mediator.handle_query(ChessGameQuery(game_id=game_id))

        return next(iter(query_result))
    except Exception as e:
        logger.error(f"Error getting board: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))