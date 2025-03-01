import datetime

import core
from core.domain.game.chess_game import ChessGame
from core.domain.game.game_format import GameFormat
from core.domain.game.game_history import ChessGameHistory
from core.domain.game.game_settings import GameSettings
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.game_status import GameStatus
from core.domain.value_objects.game_state import GameState
from core.domain.value_objects.side import Side
from core.infrastructure.models import GameDocument
from core.infrastructure.models.game_document import GameState, HistoryItem


class GameTranslator:

    @staticmethod
    def document_to_domain(document: GameDocument) -> ChessGame:
        game_id: ChessGameId = ChessGameId(document.game_id)
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.from_string(document.format.value, document.format.time_remaining)
        history = ChessGameHistory.initialize(game_id)
        game_settings = GameSettings(game_format)
        game_state = GameState(GameStatus(document.state.status), Side(document.state.turn))

        return ChessGame(game_id, game_settings, game_state, players, history)

    @staticmethod
    def domain_to_document(game: ChessGame) -> GameDocument:
        game_state: GameState = GameState(
            captured=None,
            turn=str(game.game_state.turn),
            started=game.game_state.is_started,
            finished=game.game_state.is_finished,
            status=str(game.game_state.get_status())
        )
        game_format = core.infrastructure.models.game_document.GameFormat(
            value=game.game_settings.format.to_string(),
            time_remaining=game.game_settings.format.time_remaining
        )
        players = core.infrastructure.models.game_document.Players(
            white_id='',
            black_id=''
        )
        game_history: list[HistoryItem] = []
        new_game: GameDocument = GameDocument(
            date=datetime.datetime.now(),
            state=game_state,
            format=game_format,
            players=players,
            history=game_history,
            moves_count=0,
            result='')

        return new_game