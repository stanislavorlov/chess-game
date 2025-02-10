from fastapi import APIRouter

router = APIRouter(prefix="/piece")

@router.get("/{piece_id}")
def start(piece_id):
    return {"message": f"piece {piece_id} moved"}
