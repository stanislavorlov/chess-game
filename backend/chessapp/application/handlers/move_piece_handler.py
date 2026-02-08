import json
import logging
from typing import Annotated

from fastapi import Depends

from ...application.commands.move_piece_command import MovePieceCommand
from ...application.handlers.base_command_handler import BaseCommandHandler
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository
from ...interface.api.websockets.managers import ConnectionManager


class MovePieceHandler(BaseCommandHandler[MovePieceCommand, None]):
    def __init__(self, repository: ChessGameRepository, socket_manager: ConnectionManager, logger: logging.Logger):
        self.repository = repository
        self.socket_manager = socket_manager
        self.logger = logger

    async def handle(self, event: MovePieceCommand) -> None:
        self.logger.info('MovePieceHandler: processing move for game %s', event.game_id.value)

        game = await self.repository.find(event.game_id.value)
        game.move_piece(event.piece, event.from_, event.to)

        await self.repository.save(game)

        for event_ in game.domain_events:
            await self.socket_manager.send_all(
                str(event.game_id.value),
                json.dumps(event_.to_dict(), default=str)
            )

