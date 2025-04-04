import uuid
from typing import List

from beanie import Link

from core.domain.game.game_history import ChessGameHistory
from core.infrastructure.models.game_history_document import GameHistoryDocument


class GameHistoryTranslator:

    @staticmethod
    def document_to_domain(history_document: List[Link[GameHistoryDocument]]):

        for history_item in history_document:
            match history_item.fetch():
                case '':
                    break

        return ChessGameHistory([])

    @staticmethod
    def domain_to_document(game_id: uuid.UUID, history: ChessGameHistory):

        history_list = list()
        for history_item in history:
            history_list.append(GameHistoryDocument(
                game_id=game_id,
                sequence_number=1,
                history_item={},
                history_meta='',
                action_type=''
            ))

        return history_list