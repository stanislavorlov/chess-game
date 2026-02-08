import uuid
from datetime import datetime
from typing import Optional
from beanie import Document, TimeSeriesConfig, Granularity, PydanticObjectId
from pydantic import Field, BaseModel


class PieceModel(BaseModel):
    piece_id: uuid.UUID
    side: str
    type: str

class GameHistoryDocument(Document):
    id: Optional[PydanticObjectId] = Field(None, alias='_id')
    game_id: PydanticObjectId
    sequence_number: int
    history_time: datetime = Field(default_factory=datetime.now)
    action_date: datetime
    action_type: str
    piece: Optional[PieceModel] = None
    from_position: str
    to_position: str

    class Config:
        pass

    class Settings:
        name = "game_history"
        timeseries = TimeSeriesConfig(
            time_field="history_time",
            meta_field="action_type",
            granularity=Granularity.hours,
            bucket_max_span_seconds=2592000,
            expire_after_seconds=2
        )