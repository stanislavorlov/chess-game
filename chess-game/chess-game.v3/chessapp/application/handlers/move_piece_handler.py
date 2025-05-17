from diator.requests import RequestHandler
from chessapp.application.commands.move_piece_command import MovePieceCommand
from chessapp.application.services.movement_service import MovementService


class MovePieceHandler(RequestHandler[MovePieceCommand, None]):

    def __init__(self, movement_service: MovementService):
        self.movement_service = movement_service

    async def handle(self, event: MovePieceCommand) -> None:
        print('PieceMovedHandler got called')

        await self.movement_service.move_piece(event.game_id, event.piece, event.from_, event.to)