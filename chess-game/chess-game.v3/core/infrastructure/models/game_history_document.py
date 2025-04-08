import uuid
from datetime import datetime
from typing import Optional, Literal
from beanie import Document, TimeSeriesConfig, Granularity, Link
from pydantic import Field
from core.infrastructure.models import GameDocument


class GameHistoryDocument(Document):
    game_id: uuid.UUID
    sequence_number: int
    history_time: datetime = Field(default_factory=datetime.now)
    action_type: str
    game: Optional[Link[GameDocument]]

    class Config:
        pass

    class Settings:
        name = "game_history"
        timeseries = TimeSeriesConfig(
            time_field="history_time",
            meta_field="action_type",
            granularity=Granularity.hours,
            bucket_max_span_seconds=3600,
            expire_after_seconds=2
        )

class GameCreatedDocument(GameHistoryDocument):
    action_type: str = Field(default="game_created")

class PieceMovedDocument(GameHistoryDocument):
    action_type: str = Field(default="piece_moved")
    piece_id: uuid.UUID
    from_position: str
    to_position: str