from typing import Optional, List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field
from datetime import datetime


class GameState(BaseModel):
    # ToDo: should be restored from History
    #captured: Optional[list] = None
    turn: str
    # ToDo: should be restored from History
    #status: str

class GameFormat(BaseModel):
    value: str
    # ToDo: store start/end datetime instead of remaining time
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
    # ToDo: should be restored from history
    result: str
    #history: List[Link[GameHistoryDocument]]

    class Config:
        pass

    class Settings:
        name = "games"