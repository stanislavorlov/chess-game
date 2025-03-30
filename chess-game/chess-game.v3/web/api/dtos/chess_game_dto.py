from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator


class GameState(BaseModel):
    turn: str
    started: bool
    finished: bool

class GameFormat(BaseModel):
    value: str
    remaining_time: timedelta
    additional_time: timedelta

class Players(BaseModel):
    white_id: str
    black_id: str

class ChessGameDto(BaseModel):
    game_id: str
    moves_count: int
    date: datetime
    name: str
    state: GameState
    game_format: GameFormat
    players: Players

    # @field_validator("age")
    # def validate_age(cls, value):
    #     if value < 18:
    #         raise ValueError("Age must be at least 18")
    #     return value
