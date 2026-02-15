import datetime
from ...domain.game.chess_game import ChessGame
from ...domain.game.game_history import ChessGameHistory
from ...domain.players.player_id import PlayerId
from ...domain.players.players import Players
from ...domain.value_objects.game_format import GameFormat
from ...domain.value_objects.game_id import ChessGameId
from ...domain.value_objects.game_information import GameInformation
from ...infrastructure.models import GameDocument
from .history_document_factory import GameHistoryDocumentFactory


class ChessGameFactory:

    @staticmethod
    async def create(document: GameDocument) -> ChessGame:
        if document is None:
            return None

        game_id: ChessGameId = ChessGameId(document.id)
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.parse_string(document.format.value, document.format.time_remaining,
                                              document.format.additional_time)
        
        game_info = GameInformation(game_format, datetime.datetime.now(), document.game_name)

        history_entries = list()
        for history_document in document.history:
            history_entry = GameHistoryDocumentFactory.to_domain(history_document, document.id)
            if history_entry:
                history_entries.append(history_entry)

        return ChessGame(
            game_id=game_id, 
            information=game_info, 
            players=players, 
            history=ChessGameHistory(history_entries)
        )