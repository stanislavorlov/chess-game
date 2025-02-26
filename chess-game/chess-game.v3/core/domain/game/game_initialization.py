from typing import List

from core.domain.chessboard.file import File
from core.domain.chessboard.position import Position
from core.domain.chessboard.rank import Rank
from core.domain.events.piece_positioned import PiecePositioned
from core.domain.pieces.bishop import Bishop
from core.domain.pieces.king import King
from core.domain.pieces.knight import Knight
from core.domain.pieces.pawn import Pawn
from core.domain.pieces.queen import Queen
from core.domain.pieces.rook import Rook
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side


class GameInitialization:

    @staticmethod
    def init() -> List[PiecePositioned]:
        output = [
            PiecePositioned(position=Position(File.a(), Rank.r1()), piece=Rook(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.a(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.b(), Rank.r1()), piece=Knight(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.b(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.c(), Rank.r1()), piece=Bishop(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.c(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.d(), Rank.r1()), piece=Queen(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.d(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.e(), Rank.r1()), piece=King(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.e(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.f(), Rank.r1()), piece=Bishop(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.f(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.g(), Rank.r1()), piece=Knight(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.g(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.h(), Rank.r1()), piece=Rook(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.h(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(position=Position(File.a(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.a(), Rank.r8()), piece=Rook(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.b(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.b(), Rank.r8()), piece=Knight(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.c(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.c(), Rank.r8()), piece=Bishop(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.d(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.d(), Rank.r8()), piece=Queen(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.e(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.e(), Rank.r8()), piece=King(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.f(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.f(), Rank.r8()), piece=Bishop(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.g(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.g(), Rank.r8()), piece=Knight(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.h(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(position=Position(File.h(), Rank.r8()), piece=Rook(PieceId.generate_id(), Side.black())),
        ]

        return output