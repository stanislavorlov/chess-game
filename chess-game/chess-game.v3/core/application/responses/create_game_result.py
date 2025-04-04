from dataclasses import dataclass
from datetime import datetime, timedelta
from diator.response import Response


@dataclass(frozen=True, kw_only=True)
class GameStateQueryResult:
    turn: str
    started: bool
    finished: bool

@dataclass(frozen=True, kw_only=True)
class GameFormatQueryResult:
    value: str
    remaining_time: timedelta
    additional_time: timedelta

@dataclass(frozen=True, kw_only=True)
class PlayersQueryResult:
    white_id: str
    black_id: str

@dataclass(frozen=True, kw_only=True)
class ChessGameQueryResult(Response):
    game_id: str
    date: datetime
    name: str
    state: GameStateQueryResult
    game_format: GameFormatQueryResult
    players: PlayersQueryResult