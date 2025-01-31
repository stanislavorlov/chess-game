from application.handlers.base_handler import BaseHandler
from domain.events.player_side_selected import PlayerSideSelected


class PlayerSideSelectedHandler(BaseHandler[PlayerSideSelected]):

    def handle(self, event: PlayerSideSelected):
        # ToDo: call repository and fetch Game
        # start a game
        pass