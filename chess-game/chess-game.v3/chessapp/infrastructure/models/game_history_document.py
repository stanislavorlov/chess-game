import uuid
from datetime import datetime
from typing import Optional
from beanie import Document, TimeSeriesConfig, Granularity, Link, PydanticObjectId
from pydantic import Field, BaseModel
from chessapp.infrastructure.models.game_document import GameDocument


class GameHistoryDocument(Document):
    game_id: PydanticObjectId
    sequence_number: int
    history_time: datetime = Field(default_factory=datetime.now)
    action_type: str
    game: Link[GameDocument]

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

class GameCreatedDocument(GameHistoryDocument):
    action_type: str = Field(default="game_created")

class GameStartedDocument(GameHistoryDocument):
    action_type: str = Field(default="game_started")
    started_date: datetime

class PieceModel(BaseModel):
    piece_id: uuid.UUID
    side: str
    type: str

class PieceMovedDocument(GameHistoryDocument):
    action_type: str = Field(default="piece_moved")
    piece: PieceModel
    from_position: str
    to_position: str

class PieceCapturedDocument(GameHistoryDocument):
    action_type: str = Field(default="piece_captured")
    captured_piece: PieceModel
    piece_has_attacked: PieceModel
    from_position: str
    to_position: str