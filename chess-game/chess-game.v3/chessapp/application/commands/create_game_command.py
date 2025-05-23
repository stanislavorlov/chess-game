from dataclasses import dataclass
from diator.requests import Request
from chessapp.domain.value_objects.game_format import GameFormat
from chessapp.domain.value_objects.game_id import ChessGameId

@dataclass(frozen=True, kw_only=True)
class CreateGameCommand(Request):
    name: str
    game_id: ChessGameId
    game_format: GameFormat