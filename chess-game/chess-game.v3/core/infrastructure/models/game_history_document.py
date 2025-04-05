import uuid
from datetime import datetime
from typing import Optional
from beanie import Document, TimeSeriesConfig, Granularity, Link
from pydantic import Field
from core.infrastructure.models import GameDocument


class GameHistoryDocument(Document):
    game_id: uuid.UUID
    sequence_number: int
    history_item: object
    history_time: datetime = Field(default_factory=datetime.now)
    history_meta: str
    action_type: str
    game: Optional[Link[GameDocument]]

    class Config:
        pass

    class Settings:
        name = "game_history"
        timeseries = TimeSeriesConfig(
            time_field="history_time",
            meta_field="history_meta",
            granularity=Granularity.hours,
            bucket_max_span_seconds=3600,
            expire_after_seconds=2
        )