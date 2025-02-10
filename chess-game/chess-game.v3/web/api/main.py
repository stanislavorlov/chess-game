from fastapi import APIRouter

from web.api.routes import game_api
from web.api.routes import piece_api, move_api

api_router = APIRouter()
api_router.include_router(game_api.router)
api_router.include_router(move_api.router)
api_router.include_router(piece_api.router)