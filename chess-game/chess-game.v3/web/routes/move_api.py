from fastapi import APIRouter

router = APIRouter(prefix="/move")

@router.get("/{start_position}/{to_position}")
def start(start_position, to_position):
    return {"message": f"piece moved {start_position} {to_position}"}