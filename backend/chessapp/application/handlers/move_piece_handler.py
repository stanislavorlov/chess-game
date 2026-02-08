import json
import logging
from ...application.commands.move_piece_command import MovePieceCommand
from ...application.handlers.base_command_handler import BaseCommandHandler
from ...infrastructure.repositories.chess_game_repository import ChessGameRepository
from ...infrastructure.services.redis_service import RedisService


class MovePieceHandler(BaseCommandHandler[MovePieceCommand, None]):

    def __init__(self, repository: ChessGameRepository, redis_service: RedisService, logger: logging.Logger):
        self.repository = repository
        self.redis_service = redis_service
        self.logger = logger

    async def handle(self, event: MovePieceCommand) -> None:
        self.logger.info('MovePieceHandler: processing move for game %s', event.game_id.value)

        chess_game = await self.repository.find(event.game_id.value)
        chess_game.move_piece(event.piece, event.from_, event.to)

        await self.repository.save(chess_game)

        self.logger.info('Game events %s', chess_game.domain_events)

        # Publish domain events to Redis for distributed notification
        for event_ in chess_game.domain_events:
            channel = f"chess-notifications:{chess_game.game_id}"
            message = json.dumps(event_.to_dict(), default=str)
            await self.redis_service.publish(channel, message)
