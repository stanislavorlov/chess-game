from application.handlers.base_handler import BaseHandler
from domain.events.position_selected import PositionSelected


class PositionSelectedHandler(BaseHandler[PositionSelected]):

    def handle(self, event: PositionSelected):
        pass