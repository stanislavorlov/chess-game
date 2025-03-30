import uuid
from typing import Optional
from beanie import Document
from pydantic import BaseModel
from datetime import datetime

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

class HistoryItem(BaseModel):
    move: str
    piece_id: str

class GameDocument(Document):
    game_id: uuid.UUID
    moves_count: int
    date: datetime
    game_name: str
    state: GameState
    format: GameFormat
    players: Players
    history: Optional[list] = None
    result: str

    class Config:
        pass

    class Settings:
        # the name of the collection
        name = "games"