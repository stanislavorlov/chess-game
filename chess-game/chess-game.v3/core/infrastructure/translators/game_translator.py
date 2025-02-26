import datetime

import core
from core.domain.game.chess_game import ChessGame
from core.domain.game.game_format import GameFormat
from core.domain.game.game_history import ChessGameHistory
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.infrastructure.models import GameDocument
from core.infrastructure.models.game_document import GameState, HistoryItem


class GameTranslator:

    @staticmethod
    def document_to_domain(document: GameDocument) -> ChessGame:
        game_id: ChessGameId = ChessGameId(document.game_id)
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.from_string(document.format.value, document.format.time_remaining)
        history = ChessGameHistory.empty()

        return ChessGame(game_id, game_format, history)

    @staticmethod
    def domain_to_document(game: ChessGame) -> GameDocument:
        game_state: GameState = GameState(
            captured=None,
            turn='',
            started=False,
            finished=False,
            status=''
        )
        game_format = core.infrastructure.models.game_document.GameFormat(
            value='',
            time_remaining=''
        )
        players = core.infrastructure.models.game_document.Players(
            white_id='',
            black_id=''
        )
        game_history: list[HistoryItem] = []
        new_game: GameDocument = GameDocument(
            game_id=game.game_id.value(),
            date=datetime.datetime.now(),
            state=game_state,
            format=game_format,
            players=players,
            history=game_history,
            moves_count=0,
            result='')

        return new_game