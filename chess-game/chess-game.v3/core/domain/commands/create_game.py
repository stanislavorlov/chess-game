from dataclasses import dataclass

from diator.requests import Request

from core.domain.game.game_format import GameFormat


@dataclass(frozen=True, kw_only=True)
class CreateGameCommand(Request):
    format_: GameFormat