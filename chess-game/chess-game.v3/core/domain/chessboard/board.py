from typing import List

from diator.events import DomainEvent

from core.domain.chessboard.position import Position
from core.domain.events.king_checked import KingChecked
from core.domain.events.king_checkmated import KingCheckMated
from core.domain.events.pawn_promoted import PawnPromoted
from core.domain.events.piece_captured import PieceCaptured
from core.domain.events.piece_moved import PieceMoved
from core.domain.events.piece_positioned import PiecePositioned
from core.domain.game.game_history import ChessGameHistory
from core.domain.movements.movement import Movement
from core.domain.pieces.piece import Piece


class Board:

    def __init__(self):
        self._board: dict[Position, Piece] = {}

    def reply(self, game_history: ChessGameHistory):
        for domain_event in game_history:
            self.apply(domain_event)

    def apply(self, domain_event: DomainEvent):
        match domain_event:
            case PiecePositioned() as event:
                self.piece_positioned(event)

            case PieceMoved() as event:
                self.piece_moved(event)

            case PieceCaptured() as event:
                self.piece_captured(event)

            case PawnPromoted() as event:
                self.pawn_promoted(event)

            case KingChecked() as event:
                self.king_checked(event)

            case KingCheckMated() as event:
                self.king_checkmated(event)

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

    def piece_captured(self, piece_captured: PieceCaptured):
        pass

    def pawn_promoted(self, pawn_promoted: PawnPromoted):
        pass

    def king_checked(self, king_checked: KingChecked):
        pass

    def king_checkmated(self, king_checkmated: KingCheckMated):
        pass

    def search_available_moves(self) -> List[Movement]:
        list_of_moves = []

        # ToDo: bitboard
        # https://github.com/cglouch/snakefish/blob/master/src/tables.py
        # https://www.frayn.net/beowulf/theory.html#bitboards

        # ToDo: stockfish
        # https://official-stockfish.github.io/docs/stockfish-wiki/Developers.html

        for position, piece in self._board.items():
            move = Movement()

            list_of_moves.append(move)

        return list_of_moves