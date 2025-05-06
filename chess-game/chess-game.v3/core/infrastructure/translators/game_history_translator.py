from typing import List
from beanie import PydanticObjectId
from core.domain.chessboard.position import Position
from core.domain.events.game_created import GameCreated
from core.domain.events.piece_moved import PieceMoved
from core.domain.events.piece_moved_completed import PieceMovedCompleted
from core.domain.game.game_history import ChessGameHistory
from core.domain.game.history_entry import ChessGameHistoryEntry
from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.history_entry_id import HistoryEntryId
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side
from core.infrastructure.models import GameDocument
from core.infrastructure.models.game_history_document import GameCreatedDocument, \
    PieceMovedDocument, PieceModel


class GameHistoryTranslator:

    @staticmethod
    def document_to_domain(
            game_created_docs: list[GameCreatedDocument],
            piece_moved_docs: list[PieceMovedDocument]):

        history: List[ChessGameHistoryEntry] = []

        for game_created_doc in game_created_docs:
            history.append(ChessGameHistoryEntry(
                entry_id=HistoryEntryId(game_created_doc.id),
                sequence_number=game_created_doc.sequence_number,
                history_event=GameCreated(game_id=ChessGameId(game_created_doc.game_id))
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

        return history_list