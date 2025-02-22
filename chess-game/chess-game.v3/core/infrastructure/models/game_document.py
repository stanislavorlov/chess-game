import uuid

from beanie import Document
from pydantic import BaseModel, Field
import datetime

class GameState(BaseModel):
    captured: []
    turn: str
    started: bool
    finished: bool
    status: str
    piece_positions: []

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
    game_id: uuid.uuid4 = Field(default_factory=uuid.uuid4)
    name: str
    date: datetime.datetime
    status: str
    state: GameState
    format: GameFormat
    players: Players
    history: []

    class Config:
        pass

    class Settings:
        # the name of the collection
        name = "games"