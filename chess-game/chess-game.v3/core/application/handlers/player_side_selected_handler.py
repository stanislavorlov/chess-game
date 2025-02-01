from core.application.handlers.base_handler import BaseHandler
from core.domain.events.player_side_selected import PlayerSideSelected


class PlayerSideSelectedHandler(BaseHandler[PlayerSideSelected]):

    def handle(self, event):
        # ToDo: call repository and fetch Game
        # start a game
        pass