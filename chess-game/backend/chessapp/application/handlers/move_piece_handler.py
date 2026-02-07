from typing import Annotated

from fastapi import Depends

from chessapp.application.commands.move_piece_command import MovePieceCommand
from chessapp.application.handlers.base_command_handler import BaseCommandHandler
from chessapp.application.services.movement_service import MovementService
from chessapp.interface.api.websockets.managers import ConnectionManager


class MovePieceHandler(BaseCommandHandler[MovePieceCommand, None]):
    movement_service: MovementService
    socket_manager: ConnectionManager

    async def handle(self, event: MovePieceCommand) -> None:
        print('PieceMovedHandler got called')

        await self.movement_service.move_piece(event.game_id, event.piece, event.from_, event.to)

        await self.socket_manager.send_all(str(event.game_id.value), 'Ya perdole kurwa!')

