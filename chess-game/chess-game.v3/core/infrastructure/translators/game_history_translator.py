import uuid
from typing import List

import bson
from beanie import Link
from watchfiles import awatch

from core.domain.game.game_history import ChessGameHistory
from core.infrastructure.models import GameDocument
from core.infrastructure.models.game_history_document import GameHistoryDocument


class GameHistoryTranslator:

    @staticmethod
    def document_to_domain(history_document: List[GameHistoryDocument]):

        for history_item in history_document:
            match history_item.action_type:
                case '':
                    break

        return ChessGameHistory([])

    @staticmethod
    def domain_to_document(game_id: uuid.UUID, game: GameDocument, history: ChessGameHistory):

        history_list = list()
        for history_item in history:
            history_list.append(GameHistoryDocument(
                game_id=game_id,
                sequence_number=1,
                history_item={},
                history_meta='',
                action_type='',
                game=game.link_from_id(bson.Binary.from_uuid(game_id))
            ))

        return history_list