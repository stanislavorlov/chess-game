import dataclasses
from dataclasses import dataclass
from datetime import datetime, timedelta
from ...domain.kernel.base import BaseResponse


@dataclass(frozen=True, kw_only=True)
class GameStateDto:
    turn: str
    started: bool
    finished: bool
    check_side: str
    check_position: str
    legal_moves: list = dataclasses.field(default_factory=list)

@dataclass(frozen=True, kw_only=True)
class GameFormatDto:
    value: str
    remaining_time: float
    additional_time: float

@dataclass(frozen=True, kw_only=True)
class PlayersDto:
    white_id: str
    black_id: str

@dataclass(frozen=True, kw_only=True)
class ChessGameDto(BaseResponse):
    game_id: str
    date: datetime
    name: str
    status: str
    state: GameStateDto
    game_format: GameFormatDto
    players: PlayersDto
    board: list
    history: list