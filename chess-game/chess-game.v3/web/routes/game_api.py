from fastapi import APIRouter

router = APIRouter(prefix="/game")

@router.get("/{game_id}")
def start(game_id):
    return {"message": f"game {game_id} started"}
