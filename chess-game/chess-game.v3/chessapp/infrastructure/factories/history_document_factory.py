from chessapp.domain.events.game_created import GameCreated
from chessapp.domain.events.game_started import GameStarted
from chessapp.domain.events.piece_captured import PieceCaptured
from chessapp.domain.events.piece_moved_completed import PieceMovedCompleted
from chessapp.domain.game.chess_game import ChessGame
from chessapp.domain.value_objects.history_entry_id import HistoryEntryId
from chessapp.infrastructure.models import GameDocument
from chessapp.infrastructure.models.game_history_document import GameCreatedDocument, GameStartedDocument, \
    PieceMovedDocument, PieceModel, PieceCapturedDocument


class GameHistoryDocumentFactory:

    @staticmethod
    async def create(game: ChessGame, game_doc: GameDocument) -> list:
        history_list = list()
        game_id = game.game_id.value

        for history_entry in game.history:
            if history_entry.id == HistoryEntryId.empty():
                match history_entry.action_type:
                    case GameCreated.__name__:
                        history_list.append(GameCreatedDocument(
                            game_id=game_id,
                            sequence_number=history_entry.sequence_number,
                            game=game_doc.link_from_id(game_id)
                        ))
                    case GameStarted.__name__:
                        history_list.append(GameStartedDocument(
                            game_id=game_id,
                            sequence_number=history_entry.sequence_number,
                            game=game_doc.link_from_id(game_id),
                            started_date=history_entry.history_event.started_date
                        ))
                    case PieceMovedCompleted.__name__:
                        history_list.append(PieceMovedDocument(
                            game_id=game_id,
                            sequence_number=history_entry.sequence_number,
                            game=game_doc.link_from_id(game_id),
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
                            game=game_doc.link_from_id(game_id),
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