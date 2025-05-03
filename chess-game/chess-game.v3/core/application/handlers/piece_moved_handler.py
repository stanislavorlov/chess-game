from diator.requests import RequestHandler
from core.domain.events.piece_moved import PieceMoved
from core.domain.players.player_id import PlayerId
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class PieceMovedHandler(RequestHandler[PieceMoved, None]):

    def __init__(self, repository: ChessGameRepository):
        self.repository = repository

    async def handle(self, event: PieceMoved) -> None:
        print('PieceMovedHandler got called')

        game = await self.repository.find(event.game_id.value)
        game.move_piece(PlayerId(''), event.from_, event.to)

        await self.repository.save(game)