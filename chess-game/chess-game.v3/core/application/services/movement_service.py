from core.domain.chessboard.position import Position
from core.domain.movements.movement import Movement
from core.domain.movements.movement_intent_factory import MovementIntentFactory
from core.domain.movements.movement_specification import MovementSpecification
from core.domain.pieces.piece import Piece
from core.domain.value_objects.game_id import ChessGameId
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class MovementService:

    def __init__(self, repo: ChessGameRepository):
        self.repository = repo

    async def move_piece(self, game_id: ChessGameId, piece: Piece, from_: Position, to: Position):
        game = await self.repository.find(game_id.value)

        movement: Movement = Movement(piece, from_, to)

        movement_specification = MovementSpecification(piece.get_rule())
        movement_intent = MovementIntentFactory.create(movement)

        if movement_specification.is_satisfied_by(movement_intent):
            print('Specification satisfied')
            game.move_piece(movement.piece, movement.from_position, movement.to_position)

        await self.repository.save(game)