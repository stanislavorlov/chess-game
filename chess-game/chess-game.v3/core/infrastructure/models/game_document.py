from typing import Optional, List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field
from datetime import datetime


class GameState(BaseModel):
    captured: Optional[list] = None
    turn: str
    status: str

class GameFormat(BaseModel):
    value: str
    time_remaining: str
    additional_time: str

class Players(BaseModel):
    white_id: str
    black_id: str

class GameDocument(Document):
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    date: datetime
    game_name: str
    state: GameState
    format: GameFormat
    players: Players
    # ToDo: provide a ref in HistoryDocument
    # https://beanie-odm.dev/tutorial/inserting-into-the-database/
    # history: List[Link[GameHistoryDocument]] # = Field(default_factory=list)
    result: str

    class Config:
        pass

    class Settings:
        name = "games"