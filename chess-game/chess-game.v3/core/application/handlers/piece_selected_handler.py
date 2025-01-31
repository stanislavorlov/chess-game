from core.application.handlers.base_handler import BaseHandler, T
from core.domain.events.piece_selected import PieceSelected


class PieceSelectedHandler(BaseHandler[PieceSelected]):

    def handle(self, event: PieceSelected):
        pass