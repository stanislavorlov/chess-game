from diator.requests import RequestHandler
from chessapp.application.commands.move_piece_command import MovePieceCommand
from chessapp.application.services.movement_service import MovementService
from chessapp.interface.api.websockets.managers import BaseConnectionManager


class MovePieceHandler(RequestHandler[MovePieceCommand, None]):

    def __init__(self,
                 movement_service: MovementService,
                 connection_manager: BaseConnectionManager):
        self.movement_service = movement_service
        self.socket_manager = connection_manager

    async def handle(self, event: MovePieceCommand) -> None:
        print('PieceMovedHandler got called')

        await self.movement_service.move_piece(event.game_id, event.piece, event.from_, event.to)

        await self.socket_manager.send_all(str(event.game_id.value), 'Ya perdole kurwa!')

