from diator.requests import RequestHandler

from core.domain.events.piece_moved import PieceMoved
from core.infrastructure.repositories.chess_game_repository import ChessGameRepository


class PieceMovedHandler(RequestHandler[PieceMoved, None]):

    def __init__(self, repository: ChessGameRepository):
        pass

    async def handle(self, event: PieceMoved) -> None:
        print('PieceMovedHandler got called')