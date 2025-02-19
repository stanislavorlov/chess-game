from beanie import Document
from pydantic import BaseModel
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
    time_remaining: int

class Players(BaseModel):
    white_id: str
    black_id: str

class HistoryItem(BaseModel):
    move: str
    piece_id: str

class GameDocument(Document):
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