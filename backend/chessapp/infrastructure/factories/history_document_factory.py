import datetime
from ...domain.events.game_created import GameCreated
from ...domain.events.game_started import GameStarted
from ...domain.events.piece_captured import PieceCaptured
from ...domain.events.piece_move_failed import PieceMoveFailed
from ...domain.events.piece_moved import PieceMoved
from ...domain.game.chess_game import ChessGame
from ...infrastructure.models import GameHistoryDocument
from ...infrastructure.models.game_history_document import PieceModel


class GameHistoryDocumentFactory:

    @staticmethod
    async def create(game: ChessGame) -> list[GameHistoryDocument]:
        history_list : list[GameHistoryDocument] = list()
        game_id = game.game_id.value

        for history_entry in game.history:

            history_document = GameHistoryDocument(
                _id=history_entry.id.value,
                game_id=game_id,
                sequence_number=history_entry.sequence_number,
                action_type='',
                action_date=datetime.datetime.now(),
                piece=None,
                from_position='',
                to_position='',
            )

            match history_entry.action_type:
                case GameCreated.__name__:
                    history_document.action_type = GameCreated.__name__

                case GameStarted.__name__:
                    history_document.action_type = GameStarted.__name__
                    history_document.action_date = history_entry.history_event.started_date

                case PieceMoved.__name__ | PieceCaptured.__name__:
                    history_document.action_type = history_entry.action_type
                    history_document.from_position = str(history_entry.history_event.from_)
                    history_document.to_position = str(history_entry.history_event.to)
                    history_document.piece = PieceModel(
                            piece_id=history_entry.history_event.piece.get_piece_id().value,
                            side=history_entry.history_event.piece.get_side().value(),
                            type=history_entry.history_event.piece.get_piece_type(),
                        )
                case PieceMoveFailed.__name__:
                    history_document.action_type = history_entry.action_type
                    history_document.from_position = str(history_entry.history_event.from_)
                    history_document.to_position = str(history_entry.history_event.to)
                    history_document.piece = PieceModel(
                        piece_id=history_entry.history_event.piece.get_piece_id().value,
                        side=history_entry.history_event.piece.get_side().value(),
                        type=history_entry.history_event.piece.get_piece_type(),
                    )

            history_list.append(history_document)

        return history_list