from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository

router = APIRouter(prefix="/game")

@router.get("/{game_id}")
async def start(game_id: PydanticObjectId, repository: ChessGameRepository = Depends(ChessGameRepository)):
    game = await repository.find(game_id)

    return {
        "status": 200,
        "data": game
    }
