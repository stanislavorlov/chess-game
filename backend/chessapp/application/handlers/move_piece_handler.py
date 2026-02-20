import logging
from ...application.commands.move_piece_command import MovePieceCommand
from ...application.handlers.base_command_handler import BaseCommandHandler
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository
from ...infrastructure.mediator.mediator import Mediator


class MovePieceHandler(BaseCommandHandler[MovePieceCommand, None]):

    def __init__(self, repository: ChessGameRepository, mediator: Mediator, logger: logging.Logger):
        self.repository = repository
        self.mediator = mediator
        self.logger = logger

    async def handle(self, event: MovePieceCommand) -> None:
        self.logger.info('MovePieceHandler: processing move from %s to %s for game %s', str(event.from_), str(event.to), event.game_id.value)

        chess_game = await self.repository.find(event.game_id.value)
        # Move piece now only requires from and to positions
        chess_game.move_piece(event.from_, event.to)

        await self.repository.save(chess_game)

        # Dispatch domain events collected in the aggregate
        await self.mediator.dispatch_events(chess_game)
