from core.domain.chessboard.file import File
from core.domain.chessboard.rank import Rank
from core.domain.chessboard.position import Position
from core.domain.game.chess_game import ChessGame
from core.domain.pieces.bishop import Bishop
from core.domain.pieces.king import King
from core.domain.pieces.knight import Knight
from core.domain.pieces.pawn import Pawn
from core.domain.pieces.queen import Queen
from core.domain.pieces.rook import Rook
from core.domain.rules.game_rule import GameRule
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side


class SetupRule(GameRule):

    def __init__(self, game: ChessGame):
        super().__init__()
        self._game = game

    def invoke(self):
        for file_idx, file in enumerate(File.a()):
            for rank_idx, rank in enumerate(Rank.r1()):
                if Rank.r2() < rank < Rank.r7():
                    continue

                side = Side.white() if rank.to_index() < 4 else Side.black()
                if rank in (Rank.r2(), Rank.r7()):
                    self._game.place_piece(Pawn(PieceId.generate_id(), side), Position(file, rank))
                elif rank in (Rank.r1(), Rank.r8()):
                    if file in (File.a(), File.h()):
                        self._game.place_piece(Rook(PieceId.generate_id(), side), Position(file, rank))
                    elif file in (File.b(), File.g()):
                        self._game.place_piece(Knight(PieceId.generate_id(), side), Position(file, rank))
                    elif file in (File.c(), File.f()):
                        self._game.place_piece(Bishop(PieceId.generate_id(), side), Position(file, rank))
                    elif file == File.d():
                        self._game.place_piece(Queen(PieceId.generate_id(), side), Position(file, rank))
                    else:
                        self._game.place_piece(King(PieceId.generate_id(), side), Position(file, rank))