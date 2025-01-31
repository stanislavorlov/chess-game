from application.handlers.base_handler import BaseHandler, T
from domain.events.piece_selected import PieceSelected


class PieceSelectedHandler(BaseHandler[PieceSelected]):

    def handle(self, event: PieceSelected):
        pass