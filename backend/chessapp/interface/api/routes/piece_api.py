from fastapi import APIRouter

router = APIRouter(prefix="/api/piece")

@router.get("/{piece_id}")
def start(piece_id):
    return {"message": f"piece {piece_id} moved"}
