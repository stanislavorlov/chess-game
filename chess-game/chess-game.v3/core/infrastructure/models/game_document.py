import uuid
from typing import Optional, List
from beanie import Document, Link
from pydantic import BaseModel
from datetime import datetime
from core.infrastructure.models.game_history_document import GameHistoryDocument


class GameState(BaseModel):
    captured: Optional[list] = None
    turn: str
    started: bool
    finished: bool
    status: str

class GameFormat(BaseModel):
    value: str
    time_remaining: str
    additional_time: str

class Players(BaseModel):
    white_id: str
    black_id: str

class GameDocument(Document):
    game_id: uuid.UUID
    moves_count: int
    date: datetime
    game_name: str
    state: GameState
    format: GameFormat
    players: Players
    history: List[Link[GameHistoryDocument]]
    result: str

    class Config:
        pass

    class Settings:
        name = "games"