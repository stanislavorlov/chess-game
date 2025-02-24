from diator.events import EventHandler

from core.domain.events.piece_positioned import PiecePositioned


class PiecePositionedHandler(EventHandler[PiecePositioned]):

    def __init__(self):
        pass

    async def handle(self, event: PiecePositioned):
        pass