import datetime
from chessapp.domain.chessboard.position import Position
from chessapp.domain.events.game_created import GameCreated
from chessapp.domain.events.game_started import GameStarted
from chessapp.domain.events.piece_captured import PieceCaptured
from chessapp.domain.events.piece_moved import PieceMoved
from chessapp.domain.game.chess_game import ChessGame
from chessapp.domain.game.game_history import ChessGameHistory
from chessapp.domain.game.history_entry import ChessGameHistoryEntry
from chessapp.domain.pieces.piece_factory import PieceFactory
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.players.player_id import PlayerId
from chessapp.domain.players.players import Players
from chessapp.domain.value_objects.game_format import GameFormat
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.value_objects.game_information import GameInformation
from chessapp.domain.value_objects.history_entry_id import HistoryEntryId
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side
from chessapp.infrastructure.models import GameDocument, GameHistoryDocument


class ChessGameFactory:

    @staticmethod
    async def create(document: GameDocument) -> ChessGame:
        game_id: ChessGameId = ChessGameId(document.id)
        players = Players(PlayerId(document.players.white_id), PlayerId(document.players.black_id))
        game_format = GameFormat.parse_string(document.format.value, document.format.time_remaining,
                                              document.format.additional_time)
        game_info = GameInformation(game_format, datetime.datetime.now(), document.game_name)

        history_entries = list()
        for history in document.history:
            history_document: GameHistoryDocument = history
            history_event = None

            match history_document.action_type:
                case GameCreated.__name__:
                    history_event = GameCreated(
                        game_id=game_id,
                    )
                case GameStarted.__name__:
                    history_event = GameStarted(
                        game_id=game_id,
                        started_date=history_document.action_date,
                    )
                case PieceMoved.__name__ :
                    history_event = PieceMoved(
                        game_id=game_id,
                        piece=PieceFactory.create(
                            PieceId(str(history_document.piece.piece_id)),
                            Side(history_document.piece.side),
                            PieceType.value_of(history_document.piece.type),
                        ),
                        from_=Position.parse(history_document.from_position),
                        to=Position.parse(history_document.to_position),
                    )
                case PieceCaptured.__name__:
                    history_event = PieceCaptured(
                        game_id=game_id,
                        piece=PieceFactory.create(
                            PieceId(str(history_document.piece.piece_id)),
                            Side(history_document.piece.side),
                            PieceType.value_of(history_document.piece.type),
                        ),
                        from_=Position.parse(history_document.from_position),
                        to=Position.parse(history_document.to_position),
                    )

            history_entries.append(ChessGameHistoryEntry(
                entry_id=HistoryEntryId(history_document.id),
                sequence_number=history_document.sequence_number,
                history_event=history_event
            ))

        return ChessGame(game_id, game_info, players, ChessGameHistory(history_entries))