from typing import List
from beanie import PydanticObjectId
from chessapp.domain.chessboard.position import Position
from chessapp.domain.events.game_created import GameCreated
from chessapp.domain.events.game_started import GameStarted
from chessapp.domain.events.piece_captured import PieceCaptured
from chessapp.domain.events.piece_moved import PieceMoved
from chessapp.domain.events.piece_moved_completed import PieceMovedCompleted
from chessapp.domain.game.game_history import ChessGameHistory
from chessapp.domain.game.history_entry import ChessGameHistoryEntry
from chessapp.domain.pieces.piece import Piece
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.value_objects.history_entry_id import HistoryEntryId
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side
from chessapp.infrastructure.models.game_document import GameDocument
from chessapp.infrastructure.models.game_history_document import GameCreatedDocument, \
    PieceMovedDocument, PieceModel, GameStartedDocument, PieceCapturedDocument


class GameHistoryTranslator:

    @staticmethod
    def document_to_domain(
            game_created_docs: list[GameCreatedDocument],
            game_started_docs: list[GameStartedDocument],
            piece_moved_docs: list[PieceMovedDocument],
            piece_captured_docs: list[PieceCapturedDocument]):

        history: List[ChessGameHistoryEntry] = []

        for game_created_doc in game_created_docs:
            history.append(ChessGameHistoryEntry(
                entry_id=HistoryEntryId(game_created_doc.id),
                sequence_number=game_created_doc.sequence_number,
                history_event=GameCreated(game_id=ChessGameId(game_created_doc.game_id))
            ))

        for game_started_doc in game_started_docs:
            history.append(ChessGameHistoryEntry(
                entry_id=HistoryEntryId(game_started_doc.id),
                sequence_number=game_started_doc.sequence_number,
                history_event=GameStarted(
                    game_id=ChessGameId(game_started_doc.game_id),
                    started_date=game_started_doc.started_date)
            ))

        for piece_moved_doc in piece_moved_docs:
            history.append(ChessGameHistoryEntry(
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
                )
            )

        for piece_captured_doc in piece_captured_docs:
            history.append(ChessGameHistoryEntry(
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

        return ChessGameHistory(history)

    @staticmethod
    def domain_to_document(game_id: PydanticObjectId, game: GameDocument, history: ChessGameHistory):
        history_list = list()

        for history_entry in history:
            if history_entry.id == HistoryEntryId.empty():
                match history_entry.action_type:
                    case GameCreated.__name__:
                        history_list.append(GameCreatedDocument(
                            game_id=game_id,
                            sequence_number=history_entry.sequence_number,
                            game=game.link_from_id(game_id)
                        ))
                    case GameStarted.__name__:
                        history_list.append(GameStartedDocument(
                            game_id=game_id,
                            sequence_number=history_entry.sequence_number,
                            game=game.link_from_id(game_id),
                            started_date=history_entry.history_event.started_date
                        ))
                    case PieceMovedCompleted.__name__:
                        history_list.append(PieceMovedDocument(
                            game_id=game_id,
                            sequence_number=history_entry.sequence_number,
                            game=game.link_from_id(game_id),
                            from_position=str(history_entry.history_event.from_),
                            to_position=str(history_entry.history_event.to),
                            piece=PieceModel(
                                piece_id=history_entry.history_event.piece.get_piece_id().value,
                                side=history_entry.history_event.piece.get_side().value(),
                                type=history_entry.history_event.piece.get_piece_type(),
                            )
                        ))
                    case PieceCaptured.__name__:
                        history_list.append(PieceCapturedDocument(
                            game_id=game_id,
                            sequence_number=history_entry.sequence_number,
                            game=game.link_from_id(game_id),
                            from_position=str(history_entry.history_event.from_),
                            to_position=str(history_entry.history_event.to),
                            captured_piece=PieceModel(
                                piece_id=history_entry.history_event.captured.get_piece_id().value,
                                side=history_entry.history_event.captured.get_side().value(),
                                type=history_entry.history_event.captured.get_piece_type(),
                            ),
                            piece_has_attacked=PieceModel(
                                piece_id=history_entry.history_event.attacked.get_piece_id().value,
                                side=history_entry.history_event.attacked.get_side().value(),
                                type=history_entry.history_event.attacked.get_piece_type(),
                            )
                        ))

        return history_list