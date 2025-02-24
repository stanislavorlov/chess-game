from diator.events import DomainEvent

from core.domain.chessboard.position import Position
from core.domain.events.king_checked import KingChecked
from core.domain.events.king_checkmated import KingCheckMated
from core.domain.events.pawn_promoted import PawnPromoted
from core.domain.events.piece_captured import PieceCaptured
from core.domain.events.piece_moved import PieceMoved
from core.domain.events.piece_positioned import PiecePositioned
from core.domain.game.game_history import ChessGameHistory
from core.domain.pieces.piece import Piece


class Board:

    def __init__(self):
        self._board: dict[Position, Piece] = {}

    @staticmethod
    def replay(history: ChessGameHistory):
        board = Board()
        for history_event in history:
            board.apply(history_event)

        return board

    def apply(self, domain_event: DomainEvent):
        match domain_event:
            # event occurred during the game initialization
            case PiecePositioned() as event:
                self.piece_positioned(event)

            case PieceMoved() as event:
                self.piece_moved(event)

            case PieceCaptured() as event:
                pass

            case PawnPromoted() as event:
                pass

            case KingChecked() as event:
                print('king checked')

            case KingCheckMated() as event:
                print('king checkmated')

    def piece_positioned(self, piece_positioned: PiecePositioned):
        piece = piece_positioned.piece
        position = piece_positioned.position

        self._board[position] = piece

    def piece_moved(self, piece_moved: PieceMoved):
        piece = piece_moved.piece
        from_ = piece_moved.from_
        to = piece_moved.to

        del self._board[from_]
        self._board[to] = piece