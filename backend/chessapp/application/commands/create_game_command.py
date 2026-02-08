from dataclasses import dataclass
from ...domain.kernel.base import BaseCommand
from ...domain.value_objects.game_format import GameFormat
from ...domain.value_objects.game_id import ChessGameId

@dataclass(frozen=True, kw_only=True)
class CreateGameCommand(BaseCommand):
    name: str
    game_id: ChessGameId
    game_format: GameFormat