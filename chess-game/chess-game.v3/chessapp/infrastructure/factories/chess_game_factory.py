import datetime
from chessapp.domain.game.chess_game import ChessGame
from chessapp.domain.game.game_history import ChessGameHistory
from chessapp.domain.game.history_entry import ChessGameHistoryEntry
from chessapp.domain.players.player_id import PlayerId
from chessapp.domain.players.players import Players
from chessapp.domain.value_objects.game_format import GameFormat
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.value_objects.game_information import GameInformation
from chessapp.domain.value_objects.history_entry_id import HistoryEntryId
from chessapp.infrastructure.models import GameDocument


class ChessGameFactory:

    @staticmethod
    async def create(document: GameDocument) -> ChessGame:
        game_id: ChessGameId = ChessGameId(document.id)
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.parse_string(document.format.value, document.format.time_remaining,
                                              document.format.additional_time)
        game_info = GameInformation(game_format, datetime.datetime.now(), document.game_name)

        #resolved_docs = [await link.fetch() for link in document.history]
        print('game history')
        print(document.history)

        history_entries = list()
        for history in document.history:
            history_entries.append(ChessGameHistoryEntry(
                entry_id=HistoryEntryId(history.id),
                sequence_number=history.sequence_number,
                history_event=None
            ))

        return ChessGame(game_id, game_info, players, ChessGameHistory(history_entries))