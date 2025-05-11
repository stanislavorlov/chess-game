from diator.requests import RequestHandler
from chessapp.application.services.movement_service import MovementService
from chessapp.domain.events.piece_moved import PieceMoved


class PieceMovedHandler(RequestHandler[PieceMoved, None]):

    def __init__(self, movement_service: MovementService):
        self.movement_service = movement_service

    async def handle(self, event: PieceMoved) -> None:
        print('PieceMovedHandler got called')

        await self.movement_service.move_piece(event.game_id, event.piece, event.from_, event.to)