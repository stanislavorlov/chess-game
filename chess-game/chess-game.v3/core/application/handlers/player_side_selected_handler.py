from diator.requests import RequestHandler
from diator.requests.request_handler import Req, Res

from core.application.handlers.base_handler import BaseHandler
from core.domain.events.player_side_selected import PlayerSideSelected


class PlayerSideSelectedHandler(RequestHandler[PlayerSideSelected, None]):

    def __init__(self):
        pass

    async def handle(self, request: PlayerSideSelected) -> None:
        pass