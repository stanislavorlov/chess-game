from typing import Optional, List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field
from chessapp.infrastructure.models import GameHistoryDocument

class GameFormat(BaseModel):
    value: str
    time_remaining: str
    additional_time: str

class Players(BaseModel):
    white_id: str
    black_id: str

class GameDocument(Document):
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    game_name: str
    format: GameFormat
    players: Players
    history: List[Link[GameHistoryDocument]]
    # new_item = await GameHistoryDocument().insert()
    # history.append(Link(new_item))

    class Config:
        pass

    class Settings:
        name = "games"