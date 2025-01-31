from application.handlers.base_handler import BaseHandler
from domain.events.player_selected import PlayerSelected


class PlayerSelectedHandler(BaseHandler[PlayerSelected]):

    def handle(self, event: PlayerSelected):
        # ToDo: call repository and fetch Game
        # start a game
        pass