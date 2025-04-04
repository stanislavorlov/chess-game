import datetime

import core
from core.domain.game.chess_game import ChessGame
from core.domain.value_objects.game_format import GameFormat
from core.domain.game.game_history import ChessGameHistory
from core.domain.game.game_settings import GameSettings
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.game_information import GameInformation
from core.domain.value_objects.game_status import GameStatus
from core.domain.value_objects.game_state import GameState
from core.domain.value_objects.side import Side
from core.infrastructure.models import GameDocument
from core.infrastructure.models.game_document import HistoryItem


class GameTranslator:

    @staticmethod
    def document_to_domain(document: GameDocument) -> ChessGame:
        game_id: ChessGameId = ChessGameId(str(document.game_id))
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.parse_string(document.format.value, document.format.time_remaining, document.format.additional_time)
        history = ChessGameHistory.initialize(game_id)
        game_settings = GameSettings(game_format)
        game_state = GameState(GameStatus(document.state.status), Side(document.state.turn))
        game_info = GameInformation(document.moves_count, document.date, document.game_name)

        return ChessGame(game_id, game_settings, game_info, game_state, players, history)

    @staticmethod
    def domain_to_document(game: ChessGame) -> GameDocument:
        game_state = core.infrastructure.models.game_document.GameState(
            captured=None,
            turn=str(game.game_state.turn),
            started=game.game_state.is_started,
            finished=game.game_state.is_finished,
            status=str(game.game_state.get_status())
        )
        game_format = core.infrastructure.models.game_document.GameFormat(
            value=game.game_settings.format.to_string(),
            time_remaining=game.game_settings.format.time_remaining.main_string(),
            additional_time=game.game_settings.format.time_remaining.additional_string()
        )
        players = core.infrastructure.models.game_document.Players(
            white_id='',
            black_id=''
        )
        game_history: list[HistoryItem] = []
        new_game: GameDocument = GameDocument(
            game_id=game.game_id.value,
            date=game.information.date,
            state=game_state,
            format=game_format,
            players=players,
            history=game_history,
            moves_count=game.information.count_of_moves,
            result='',
            game_name=game.information.name
        )

        return new_game