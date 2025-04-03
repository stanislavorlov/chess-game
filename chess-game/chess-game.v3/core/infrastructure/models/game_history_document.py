import uuid
from datetime import datetime

from beanie import Document, TimeSeriesConfig, Granularity
from pydantic import Field


class GameHistoryDocument(Document):
    game_id: uuid.UUID
    sequence_number: int
    history_item: object
    history_time: datetime = Field(default_factory=datetime.now)
    history_meta: str

    class Config:
        pass

    class Settings:
        name = "game_history"
        timeseries = TimeSeriesConfig(
            time_field="history_time",  # Required
            meta_field="history_meta",  # Optional
            granularity=Granularity.hours,  # Optional
            bucket_max_span_seconds=3600,  # Optional
            expire_after_seconds=2  # Optional
        )