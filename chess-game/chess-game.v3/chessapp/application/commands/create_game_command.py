from dataclasses import dataclass
from chessapp.domain.kernel.base import BaseCommand
from chessapp.domain.value_objects.game_format import GameFormat
from chessapp.domain.value_objects.game_id import ChessGameId

@dataclass(frozen=True, kw_only=True)
class CreateGameCommand(BaseCommand):
    name: str
    game_id: ChessGameId
    game_format: GameFormat