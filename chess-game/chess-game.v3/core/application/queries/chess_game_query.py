import dataclasses
import uuid

from diator.requests import Request


@dataclasses.dataclass(frozen=True, kw_only=True)
class ChessGameQuery(Request):
    game_id: uuid = dataclasses.field()