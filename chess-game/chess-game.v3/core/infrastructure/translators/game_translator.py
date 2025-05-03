import datetime
import core
from core.domain.game.chess_game import ChessGame
from core.domain.value_objects.game_format import GameFormat
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.game_information import GameInformation
from core.domain.value_objects.game_status import GameStatus
from core.domain.value_objects.game_state import GameState
from core.domain.value_objects.side import Side
from core.infrastructure.models import GameDocument, GameHistoryDocument
from core.infrastructure.translators.game_history_translator import GameHistoryTranslator


class GameTranslator:

    @staticmethod
    def document_to_domain(document: GameDocument, history_docs: list[GameHistoryDocument]) -> ChessGame:
        game_id: ChessGameId = ChessGameId(document.id)
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.parse_string(document.format.value, document.format.time_remaining, document.format.additional_time)

        history = GameHistoryTranslator.document_to_domain(history_docs)

        game_state = GameState(GameStatus(document.state.status), Side(document.state.turn))
        game_info = GameInformation(game_format, document.date, document.game_name)

        return ChessGame(game_id, game_info, game_state, players, history)

    @staticmethod
    def domain_to_document(game: ChessGame) -> GameDocument:
        game_state = core.infrastructure.models.game_document.GameState(
            captured=None,
            turn=str(game.game_state.turn),
            status=str(game.game_state.get_status())
        )
        game_format = core.infrastructure.models.game_document.GameFormat(
            value=game.information.format.to_string(),
            time_remaining=game.information.format.time_remaining.main_string(),
            additional_time=game.information.format.time_remaining.additional_string()
        )
        players = core.infrastructure.models.game_document.Players(
            white_id='',
            black_id=''
        )
        new_game: GameDocument = GameDocument(
            _id=game.game_id.value,
            date=game.information.date,
            state=game_state,
            format=game_format,
            players=players,
            result='',
            game_name=game.information.name
        )

        return new_game