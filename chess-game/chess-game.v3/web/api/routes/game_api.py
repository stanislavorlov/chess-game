from fastapi import APIRouter

from core.domain.commands.start_game import StartGameCommand
from core.domain.game.game_format import GameFormat
from core.infrastructure.mediator.mediator import build_mediator

router = APIRouter(prefix="/game")

@router.post("/create_board/{game_format}")
async def create_board(game_format: str):
    mediator = build_mediator()

    game_created = await mediator.send(StartGameCommand(format_=GameFormat.parse_string(game_format)))

    return {
        "status": 200,
        "data": game_created
    }