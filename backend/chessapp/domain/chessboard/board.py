from typing import List, Optional
from . import bitboard_utils as utils
from ..events.king_castled import KingCastled
from ..pieces.piece_type import PieceType
from ...domain.chessboard.file import File
from ...domain.chessboard.position import Position
from ...domain.chessboard.rank import Rank
from ...domain.chessboard.square import Square
from ...domain.events.king_checked import KingChecked
from ...domain.events.king_checkmated import KingCheckMated
from ...domain.events.pawn_promoted import PawnPromoted
from ...domain.events.piece_captured import PieceCaptured
from ...domain.events.piece_moved import PieceMoved
from ...domain.kernel.value_object import ValueObject
from ...domain.movements.movement import Movement
from ...domain.pieces.bishop import Bishop
from ...domain.pieces.king import King
from ...domain.pieces.knight import Knight
from ...domain.pieces.pawn import Pawn
from ...domain.pieces.queen import Queen
from ...domain.pieces.rook import Rook
from ...domain.value_objects.side import Side


class Board(ValueObject):

    def __init__(self):
        super().__init__()
        self._bitboard_utils = utils.BitboardUtils()
        self._board: dict[Position, Square] = {}
        # 12 bitboards for each piece type and color
        self._bitboards: dict[tuple[Side, PieceType], int] = {}
        # 3 occupancy bitboards: white, black, and combined
        self._occupancy: dict[Optional[Side], int] = {
            Side.white(): 0,
            Side.black(): 0,
            None: 0
        }
        self.__initialize_bitboards()
        self.__board_initialize__(self._board)

    def __initialize_bitboards(self):
        for side in [Side.white(), Side.black()]:
            for piece_type in PieceType:
                self._bitboards[(side, piece_type)] = 0


    def piece_moved(self, piece_moved: PieceMoved):
        piece = piece_moved.piece
        from_ = piece_moved.from_
        to = piece_moved.to

        is_castling = piece.get_piece_type() == PieceType.King and abs(to.file.to_index() - from_.file.to_index()) == 2

        piece.mark_moved()

        # Update dictionary-based board
        self._board[from_] = Square(from_, None)
        self._board[to] = Square(to, piece)

        # Update bitboards
        utils.clear_piece_bit(utils.to_bit_index(from_), piece.get_side(), piece.get_piece_type(), self._bitboards, self._occupancy)
        utils.set_piece_bit(utils.to_bit_index(to), piece.get_side(), piece.get_piece_type(), self._bitboards, self._occupancy)

        if is_castling:
            rank = from_.rank
            is_kingside = to.file.to_index() > from_.file.to_index()
            rook_from_file = File.h() if is_kingside else File.a()
            rook_to_file = File.f() if is_kingside else File.d()

            rook_from = Position(rook_from_file, rank)
            rook_to = Position(rook_to_file, rank)

            rook_sq = self._board[rook_from]
            rook = rook_sq.piece

            if rook:
                rook.mark_moved()
                # Update dictionary-based board
                self._board[rook_from] = Square(rook_from, None)
                self._board[rook_to] = Square(rook_to, rook)

                # Update bitboards
                utils.clear_piece_bit(utils.to_bit_index(rook_from), rook.get_side(), rook.get_piece_type(), self._bitboards, self._occupancy)
                utils.set_piece_bit(utils.to_bit_index(rook_to), rook.get_side(), rook.get_piece_type(), self._bitboards, self._occupancy)

    def king_castled(self, king_castled: KingCastled):
        rook = self._board[king_castled.rook_from].piece
        king = self._board[king_castled.king_from].piece
        rook_from, rook_to = king_castled.rook_from, king_castled.rook_to
        king_from, king_to = king_castled.king_from, king_castled.king_to

        self._board[rook_from] = Square(rook_from, None)
        self._board[rook_to] = Square(rook_to, rook)

        self._board[king_from] = Square(king_from, None)
        self._board[king_to] = Square(king_to, king)


    def piece_captured(self, piece_captured: PieceCaptured):
        # The PieceMoved event following this will update the square piece on 'to' position.
        # But we must clear the bit of the captured piece first.
        utils.clear_piece_bit(utils.to_bit_index(piece_captured.to), piece_captured.piece.get_side(), piece_captured.piece.get_piece_type(), self._bitboards, self._occupancy)
        pass

    def pawn_promoted(self, pawn_promoted: PawnPromoted):
        pass

    def king_checked(self, king_checked: KingChecked):
        pass

    def king_checkmated(self, king_checkmated: KingCheckMated):
        pass

    def search_available_moves(self) -> List[Movement]:
        list_of_moves = []
        
        for side in [Side.white(), Side.black()]:
            # Pawns
            list_of_moves.extend(utils.get_pawn_moves(
                side, 
                self._bitboards[(side, PieceType.Pawn)], 
                self._occupancy[None], 
                self._occupancy[Side.black() if side == Side.white() else Side.white()],
                self._bitboard_utils
            ))
            # Knights
            list_of_moves.extend(utils.get_knight_moves(
                self._bitboards[(side, PieceType.Knight)], 
                self._occupancy[side], 
                self._bitboard_utils
            ))
            # Kings
            list_of_moves.extend(utils.get_king_moves(
                self._bitboards[(side, PieceType.King)], 
                self._occupancy[side], 
                self._bitboard_utils
            ))
            
            # Castling moves
            king_pos = self.get_king_position(side)
            king = self._board[king_pos].piece if king_pos else None
            rank = Rank.r1() if side == Side.white() else Rank.r8()
            rook_h = self._board[Position(File.h(), rank)].piece
            rook_a = self._board[Position(File.a(), rank)].piece

            list_of_moves.extend(utils.get_castling_moves(
                side=side,
                king_pos=king_pos,
                king_moved=king.is_moved if king else True,
                is_check=self.is_check(side),
                rook_h_unmoved=bool(rook_h and rook_h.get_piece_type() == PieceType.Rook and not rook_h.is_moved),
                rook_a_unmoved=bool(rook_a and rook_a.get_piece_type() == PieceType.Rook and not rook_a.is_moved),
                is_square_occupied_fn=lambda pos: self._board[pos].piece is not None,
                is_square_attacked_fn=lambda pos, opp: self.is_attacked(pos, opp)
            ))

            # Sliders
            list_of_moves.extend(utils.get_sliding_moves(side, PieceType.Rook, self._bitboards[(side, PieceType.Rook)], self._occupancy[None], self._occupancy[side]))
            list_of_moves.extend(utils.get_sliding_moves(side, PieceType.Bishop, self._bitboards[(side, PieceType.Bishop)], self._occupancy[None], self._occupancy[side]))
            list_of_moves.extend(utils.get_sliding_moves(side, PieceType.Queen, self._bitboards[(side, PieceType.Queen)], self._occupancy[None], self._occupancy[side]))

        return list_of_moves


    def evaluate_board(self) -> float:
        """Basic evaluation based on material weight."""
        score = 0
        weights = {
            PieceType.Pawn: 10,
            PieceType.Knight: 30,
            PieceType.Bishop: 30,
            PieceType.Rook: 50,
            PieceType.Queen: 90,
            PieceType.King: 900
        }
        
        for (side, p_type), bb in self._bitboards.items():
            count = utils.count_bits(bb)
            val = count * weights[p_type]
            score += val if side == Side.white() else -val
            
        return score

    def is_check(self, side: Side) -> bool:
        king_pos = self.get_king_position(side)
        if king_pos is None: return False
        
        opponent_side = Side.black() if side == Side.white() else Side.white()
        return self.is_attacked(king_pos, opponent_side)

    def get_king_position(self, side: Side) -> Optional[Position]:
        king_bb = self._bitboards.get((side, PieceType.King), 0)
        if king_bb == 0: return None
        
        # Get index of the set bit using utility
        king_idx = utils.get_lsb_index(king_bb)
        return utils.bit_index_to_position(king_idx)

    def is_attacked(self, position: Position, attacking_side: Side) -> bool:
        return utils.is_square_attacked(
            square_index=utils.to_bit_index(position),
            attacking_side=attacking_side,
            bitboards=self._bitboards,
            occupancy_combined=self._occupancy[None],
            utils=self._bitboard_utils
        )

    def clone(self):
        new_board = Board.__new__(Board)
        new_board._bitboard_utils = self._bitboard_utils
        new_board._board = self._board.copy()
        new_board._bitboards = self._bitboards.copy()
        new_board._occupancy = self._occupancy.copy()
        return new_board

    def get_legal_moves(self, side: Side) -> List[Movement]:
        pseudo_legal_moves = self.search_available_moves()
        # Filter for current turn's pieces
        side_pseudo = [m for m in pseudo_legal_moves if self._board[m.from_position].piece.get_side() == side]
        
        legal_moves = []
        for move in side_pseudo:
            temp_board = self.clone()
            
            # Simulate capture if necessary
            target_piece = temp_board._board[move.to_position].piece
            if target_piece:
                temp_board.piece_captured(PieceCaptured(game_id=None, from_=move.from_position, to=move.to_position, piece=target_piece))
            
            # Simulate move
            moving_piece = temp_board._board[move.from_position].piece
            temp_board.piece_moved(PieceMoved(game_id=None, from_=move.from_position, to=move.to_position, piece=moving_piece))
            
            if not temp_board.is_check(side):
                legal_moves.append(move)
        return legal_moves

    def is_checkmate(self, side: Side) -> bool:
        return self.is_check(side) and len(self.get_legal_moves(side)) == 0

    def __board_initialize__(self, board: dict[Position, Square]):
        for file in File.a():
            for rank in Rank.r1():
                piece_color = Side.white() if rank in (Rank.r1(), Rank.r2()) else Side.black()
                position = Position(file, rank)
                piece = None

                if rank in (Rank.r2(), Rank.r7()):
                    piece = Pawn(piece_color)
                elif rank in (Rank.r1(), Rank.r8()):
                    if file in (File.a(), File.h()):
                        piece = Rook(piece_color)
                    elif file in (File.b(), File.g()):
                        piece = Knight(piece_color)
                    elif file in (File.c(), File.f()):
                        piece = Bishop(piece_color)
                    elif file == File.d():
                        piece = Queen(piece_color)
                    elif file == File.e():
                        piece = King(piece_color)
                
                board[position] = Square(position, piece)
                if piece:
                  utils.set_piece_bit(utils.to_bit_index(position), piece.get_side(), piece.get_piece_type(), self._bitboards, self._occupancy)

    def __iter__(self):
        return iter(self._board)

    def __getitem__(self, item: Position):
        return self._board[item]