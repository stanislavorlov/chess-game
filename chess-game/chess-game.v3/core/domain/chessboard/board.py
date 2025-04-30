from typing import List
from diator.events import DomainEvent
from core.domain.chessboard.file import File
from core.domain.chessboard.position import Position
from core.domain.chessboard.rank import Rank
from core.domain.chessboard.square import Square
from core.domain.events.king_checked import KingChecked
from core.domain.events.king_checkmated import KingCheckMated
from core.domain.events.pawn_promoted import PawnPromoted
from core.domain.events.piece_captured import PieceCaptured
from core.domain.events.piece_moved import PieceMoved
from core.domain.game.game_history import ChessGameHistory
from core.domain.kernel.value_object import ValueObject
from core.domain.movements.movement import Movement
from core.domain.pieces.bishop import Bishop
from core.domain.pieces.king import King
from core.domain.pieces.knight import Knight
from core.domain.pieces.pawn import Pawn
from core.domain.pieces.queen import Queen
from core.domain.pieces.rook import Rook
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side


class Board(ValueObject):

    def __init__(self):
        super().__init__()

        self._board: dict[Position, Square] = {}

        for file in File.a():
            for rank in Rank.r1():
                piece_color = Side.white() if rank in (Rank.r1(), Rank.r2()) else Side.black()
                position = Position(file, rank)

                if rank in (Rank.r2(), Rank.r7()):
                    self._board[position] = Square(position, Pawn(PieceId.generate_id(), piece_color))
                elif rank in (Rank.r1(), Rank.r8()):
                    if file in (File.a(), File.h()):
                        self._board[position] = Square(position, Rook(PieceId.generate_id(), piece_color))
                    elif file in (File.b(), File.g()):
                        self._board[position] = Square(position, Knight(PieceId.generate_id(), piece_color))
                    elif file in (File.c(), File.f()):
                        self._board[position] = Square(position, Bishop(PieceId.generate_id(), piece_color))
                    elif file == File.d():
                        self._board[position] = Square(position, Queen(PieceId.generate_id(), piece_color))
                    else:
                        self._board[position] = Square(position, King(PieceId.generate_id(), piece_color))
                else:
                    self._board[position] = Square(position, None)

    def reply(self, game_history: ChessGameHistory):
        for domain_event in game_history:
            self.apply(domain_event)

    def apply(self, domain_event: DomainEvent):
        match domain_event:

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

    def serialize(self):

        def build_piece(s: Square):
            if s.piece:
                return {
                    'piece_id': s.piece.get_piece_id().value,
                    'abbreviation': s.piece.get_abbreviation()
                }

            return None

        board_array = []
        for position in self._board:
            square = self._board[position]
            board_array.append({
                'square': str(square.position),
                'piece': build_piece(square),
                'color': str(square.color),
                'rank': square.position.rank.value
            })

        return board_array