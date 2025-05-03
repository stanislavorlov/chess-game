import json
import uuid
from typing import List
from beanie import PydanticObjectId
from core.domain.events.game_created import GameCreated
from core.domain.events.piece_moved import PieceMoved
from core.domain.game.game_history import ChessGameHistory
from core.domain.game.history_entry import ChessGameHistoryEntry
from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side
from core.infrastructure.models import GameDocument
from core.infrastructure.models.game_history_document import GameHistoryDocument, GameCreatedDocument, \
    PieceMovedDocument

class GameHistoryTranslator:

    @staticmethod
    def document_to_domain(history_document: List[GameHistoryDocument]):
        history: List[ChessGameHistoryEntry] = []
        for history_item in history_document:
            json_document = history_item.model_dump_json()
            json_obj = json.loads(json_document)

            match json_obj['action_type']:
                case GameCreatedDocument.action_type:
                    history.append(ChessGameHistoryEntry(
                        sequence_number=history_item.sequence_number,
                        history_event=GameCreated(game_id=ChessGameId(history_item.game_id))
                    ))
                case PieceMovedDocument.action_type:
                    history.append(ChessGameHistoryEntry(
                        sequence_number=history_item.sequence_number,
                        history_event=PieceMoved(
                            game_id=ChessGameId(history_item.game_id),
                            piece=Piece(PieceId(''), Side.black(), PieceType.Rook),
                            from_=json_obj['from_position'],
                            to=json_obj['to_position']
                        )
                    ))

        return ChessGameHistory(history)

    @staticmethod
    def domain_to_document(game_id: PydanticObjectId, game: GameDocument, history: ChessGameHistory):

        history_list = list()

        for history_entry in history:
            match history_entry.action_type:
                case GameCreated.__name__:
                    history_list.append(GameCreatedDocument(
                        game_id=game_id,
                        sequence_number=history_entry.sequence_number,
                        game=game.link_from_id(game_id)
                    ))
                case PieceMoved.__name__:
                    # ToDo: dict
                    history_list.append(PieceMovedDocument(
                        game_id=game_id,
                        sequence_number=history_entry.sequence_number,
                        piece_id=uuid.uuid4(),
                        game=game.link_from_id(game_id),
                        from_position='',
                        to_position=''
                    ))

        return history_list