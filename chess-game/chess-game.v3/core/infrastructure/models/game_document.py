from typing import Optional
from uuid import uuid4
from beanie import Document
from pydantic import BaseModel, Field
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

class Players(BaseModel):
    white_id: str
    black_id: str

class HistoryItem(BaseModel):
    move: str
    piece_id: str

class GameDocument(Document):
    game_id: uuid4 = Field(default_factory=uuid4)
    name: str
    date: datetime
    state: GameState
    format: GameFormat
    players: Players
    history: Optional[list] = None

    class Config:
        pass

    class Settings:
        # the name of the collection
        name = "games"