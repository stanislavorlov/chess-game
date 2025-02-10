from fastapi import APIRouter

from web.routes import game_api, move_api, piece_api

api_router = APIRouter()
api_router.include_router(game_api.router)
api_router.include_router(move_api.router)
api_router.include_router(piece_api.router)