from dataclasses import dataclass
from datetime import datetime, timedelta
from chessapp.domain.kernel.base import BaseResponse


@dataclass(frozen=True, kw_only=True)
class GameStateDto:
    turn: str
    started: bool
    finished: bool

@dataclass(frozen=True, kw_only=True)
class GameFormatDto:
    value: str
    remaining_time: timedelta
    additional_time: timedelta

@dataclass(frozen=True, kw_only=True)
class PlayersDto:
    white_id: str
    black_id: str

@dataclass(frozen=True, kw_only=True)
class ChessGameDto(BaseResponse):
    game_id: str
    date: datetime
    name: str
    state: GameStateDto
    game_format: GameFormatDto
    players: PlayersDto
    board: list
    history: list