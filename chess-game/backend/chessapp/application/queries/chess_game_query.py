import dataclasses
from chessapp.domain.kernel.base import BaseQuery
from chessapp.domain.value_objects.game_id import ChessGameId


@dataclasses.dataclass(frozen=True, kw_only=True)
class ChessGameQuery(BaseQuery):
    game_id: ChessGameId = dataclasses.field()