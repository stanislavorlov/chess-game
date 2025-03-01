from typing import List
from diator.events import DomainEvent

from core.domain.chessboard.file import File
from core.domain.chessboard.position import Position
from core.domain.chessboard.rank import Rank
from core.domain.events.piece_positioned import PiecePositioned
from core.domain.kernel.entity import Entity
from core.domain.pieces.bishop import Bishop
from core.domain.pieces.king import King
from core.domain.pieces.knight import Knight
from core.domain.pieces.pawn import Pawn
from core.domain.pieces.queen import Queen
from core.domain.pieces.rook import Rook
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side


class ChessGameHistory(Entity):

    def __init__(self, history: List[DomainEvent]):
        super().__init__()
        self._gameHistory = history
        self._startIndex = 0

    @staticmethod
    def initialize(game_id: ChessGameId):
        init_history = [
            PiecePositioned(game_id=game_id, position=Position(File.a(), Rank.r1()), piece=Rook(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.a(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.b(), Rank.r1()), piece=Knight(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.b(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.c(), Rank.r1()), piece=Bishop(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.c(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.d(), Rank.r1()), piece=Queen(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.d(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.e(), Rank.r1()), piece=King(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.e(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.f(), Rank.r1()), piece=Bishop(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.f(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.g(), Rank.r1()), piece=Knight(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.g(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.h(), Rank.r1()), piece=Rook(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.h(), Rank.r2()), piece=Pawn(PieceId.generate_id(), Side.white())),
            PiecePositioned(game_id=game_id, position=Position(File.a(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.a(), Rank.r8()), piece=Rook(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.b(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.b(), Rank.r8()), piece=Knight(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.c(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.c(), Rank.r8()), piece=Bishop(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.d(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.d(), Rank.r8()), piece=Queen(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.e(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.e(), Rank.r8()), piece=King(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.f(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.f(), Rank.r8()), piece=Bishop(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.g(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.g(), Rank.r8()), piece=Knight(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.h(), Rank.r7()), piece=Pawn(PieceId.generate_id(), Side.black())),
            PiecePositioned(game_id=game_id, position=Position(File.h(), Rank.r8()), piece=Rook(PieceId.generate_id(), Side.black()))]

        return ChessGameHistory(init_history)

    def record(self, entry: DomainEvent):
        self._gameHistory.append(entry)

    def last(self):
        return self._gameHistory[:-1]

    def __iter__(self):
        return iter(self._gameHistory)

    def __next__(self):
        history_item = self._gameHistory[self._startIndex]
        self._startIndex += 1

        return history_item