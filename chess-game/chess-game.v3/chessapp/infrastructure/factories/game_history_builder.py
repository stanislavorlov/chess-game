from chessapp.domain.chessboard.position import Position
from chessapp.domain.events.game_created import GameCreated
from chessapp.domain.events.game_started import GameStarted
from chessapp.domain.events.piece_captured import PieceCaptured
from chessapp.domain.events.piece_moved import PieceMoved
from chessapp.domain.game.history_entry import ChessGameHistoryEntry
from chessapp.domain.pieces.piece import Piece
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.value_objects.history_entry_id import HistoryEntryId
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side
from chessapp.infrastructure.models.game_history_document import GameCreatedDocument, GameStartedDocument, \
    PieceMovedDocument, PieceCapturedDocument


class ChessGameHistoryBuilder:

    def __init__(self):
        self.history = []

    def build_game_created_events(self, game_created_docs: list[GameCreatedDocument]):
        for game_created_doc in game_created_docs:
            self.history.append(ChessGameHistoryEntry(
                entry_id=HistoryEntryId(game_created_doc.id),
                sequence_number=game_created_doc.sequence_number,
                history_event=GameCreated(game_id=ChessGameId(game_created_doc.game_id))
            ))

    def build_game_started_events(self, game_started_docs: list[GameStartedDocument]):
        for game_started_doc in game_started_docs:
            self.history.append(ChessGameHistoryEntry(
                entry_id=HistoryEntryId(game_started_doc.id),
                sequence_number=game_started_doc.sequence_number,
                history_event=GameStarted(
                    game_id=ChessGameId(game_started_doc.game_id),
                    started_date=game_started_doc.started_date)
            ))

    def build_piece_moved_events(self, piece_moved_docs: list[PieceMovedDocument]):
        for piece_moved_doc in piece_moved_docs:
            self.history.append(ChessGameHistoryEntry(
                entry_id=HistoryEntryId(piece_moved_doc.id),
                sequence_number=piece_moved_doc.sequence_number,
                history_event=PieceMoved(
                    game_id=ChessGameId(piece_moved_doc.game_id),
                    piece=Piece(
                        PieceId(str(piece_moved_doc.piece.piece_id)),
                        Side(str(piece_moved_doc.piece.side)),
                        PieceType.value_of(str(piece_moved_doc.piece.type))),
                    from_=Position.parse(piece_moved_doc.from_position),
                    to=Position.parse(piece_moved_doc.to_position))
            ))

    def build_piece_captured_events(self, piece_captured_docs: list[PieceCapturedDocument]):
        for piece_captured_doc in piece_captured_docs:
            self.history.append(ChessGameHistoryEntry(
                entry_id=HistoryEntryId(piece_captured_doc.id),
                sequence_number=piece_captured_doc.sequence_number,
                history_event=PieceCaptured(
                    game_id=ChessGameId(piece_captured_doc.game_id),
                    captured=Piece(
                        PieceId(str(piece_captured_doc.captured_piece.piece_id)),
                        Side(str(piece_captured_doc.captured_piece.side)),
                        PieceType.value_of(str(piece_captured_doc.captured_piece.type))),
                    attacked=Piece(
                        PieceId(str(piece_captured_doc.piece_has_attacked.piece_id)),
                        Side(str(piece_captured_doc.piece_has_attacked.side)),
                        PieceType.value_of(str(piece_captured_doc.piece_has_attacked.type))),
                    from_=Position.parse(piece_captured_doc.from_position),
                    to=Position.parse(piece_captured_doc.to_position)
                )
            ))

    def get_history(self):
        return self.history