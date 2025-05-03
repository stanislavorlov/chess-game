import dataclasses
from diator.requests import Request
from core.domain.value_objects.game_id import ChessGameId


@dataclasses.dataclass(frozen=True, kw_only=True)
class ChessGameQuery(Request):
    game_id: ChessGameId = dataclasses.field()