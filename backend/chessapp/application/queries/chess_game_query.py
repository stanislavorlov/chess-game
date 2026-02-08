import dataclasses
from ...domain.kernel.base import BaseQuery
from ...domain.value_objects.game_id import ChessGameId


@dataclasses.dataclass(frozen=True, kw_only=True)
class ChessGameQuery(BaseQuery):
    game_id: ChessGameId = dataclasses.field()