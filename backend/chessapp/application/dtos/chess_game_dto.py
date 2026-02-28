from dataclasses import dataclass
from datetime import datetime
from ...domain.kernel.base import BaseResponse


@dataclass(frozen=True, kw_only=True)
class GameStateDto:
    turn: str
    started: bool
    finished: bool
    check_side: str
    check_position: str
    legal_moves: str = ""

@dataclass(frozen=True, kw_only=True)
class GameFormatDto:
    value: str
    white_remaining_time: float
    black_remaining_time: float
    move_increment: float

@dataclass(frozen=True, kw_only=True)
class PlayersDto:
    white_id: str
    black_id: str

@dataclass(frozen=True, kw_only=True)
class ChessGameDto(BaseResponse):
    game_id: str
    moves_count: int
    date: datetime
    name: str
    status: str
    state: GameStateDto
    game_format: GameFormatDto
    players: PlayersDto
    board: str
    history: str