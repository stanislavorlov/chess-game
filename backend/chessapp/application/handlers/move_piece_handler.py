from typing import Annotated

from fastapi import Depends

from ...application.commands.move_piece_command import MovePieceCommand
from ...application.handlers.base_command_handler import BaseCommandHandler
from ...application.services.movement_service import MovementService
from ...interface.api.websockets.managers import ConnectionManager


class MovePieceHandler(BaseCommandHandler[MovePieceCommand, None]):
    def __init__(self, movement_service: MovementService, socket_manager: ConnectionManager):
        self.movement_service = movement_service
        self.socket_manager = socket_manager

    async def handle(self, event: MovePieceCommand) -> None:
        print('PieceMovedHandler got called')

        await self.movement_service.move_piece(event.game_id, event.piece, event.from_, event.to)

        await self.socket_manager.send_all(str(event.game_id.value), 'Ya perdole kurwa!')

