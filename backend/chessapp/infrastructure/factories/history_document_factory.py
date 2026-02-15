import datetime
from typing import Optional
from beanie import PydanticObjectId
from ...domain.chessboard.position import Position
from ...domain.events.game_created import GameCreated
from ...domain.events.game_started import GameStarted
from ...domain.events.game_finished import GameFinished
from ...domain.events.king_checked import KingChecked
from ...domain.events.king_checkmated import KingCheckMated
from ...domain.events.king_castled import KingCastledEvent
from ...domain.events.piece_captured import PieceCaptured
from ...domain.events.piece_move_failed import PieceMoveFailed
from ...domain.events.piece_moved import PieceMoved
from ...domain.game.chess_game import ChessGame
from ...domain.game.history_entry import ChessGameHistoryEntry
from ...domain.pieces.piece_factory import PieceFactory
from ...domain.pieces.piece_type import PieceType
from ...domain.value_objects.game_id import ChessGameId
from ...domain.value_objects.history_entry_id import HistoryEntryId
from ...domain.value_objects.side import Side
from ...infrastructure.models import GameHistoryDocument
from ...domain.kernel.serialization import domain_to_dict


class GameHistoryDocumentFactory:

    @staticmethod
    def to_domain(history_document: GameHistoryDocument, game_id_raw: any) -> Optional[ChessGameHistoryEntry]:
        game_id = ChessGameId(PydanticObjectId(game_id_raw))
        payload = history_document.payload or {}
        
        event = None
        match history_document.action_type:
            case GameCreated.__name__:
                event = GameCreated(game_id=game_id)
            case GameStarted.__name__:
                started_date_raw = payload.get('started_date')
                event = GameStarted(
                    game_id=game_id, 
                    started_date=datetime.datetime.fromisoformat(started_date_raw) if isinstance(started_date_raw, str) else started_date_raw
                )
            case GameFinished.__name__:
                finished_date_raw = payload.get('finished_date')
                event = GameFinished(
                    game_id=game_id,
                    result=payload.get('result', ''),
                    finished_date=datetime.datetime.fromisoformat(finished_date_raw) if isinstance(finished_date_raw, str) else finished_date_raw
                )
            case PieceMoved.__name__ | PieceCaptured.__name__:
                piece_data = payload.get('piece')
                if not piece_data: return None
                
                piece = PieceFactory.create(Side(piece_data['side']), PieceType.value_of(piece_data['type']))
                from_pos = Position.parse(payload.get('from_')) if payload.get('from_') else None
                to_pos = Position.parse(payload.get('to')) if payload.get('to') else None
                
                if not piece or not from_pos or not to_pos: return None

                if history_document.action_type == PieceMoved.__name__:
                    event = PieceMoved(game_id=game_id, piece=piece, from_=from_pos, to=to_pos)
                else:
                    event = PieceCaptured(game_id=game_id, piece=piece, from_=from_pos, to=to_pos)
            
            case KingChecked.__name__ | KingCheckMated.__name__:
                side_raw = payload.get('side')
                pos_raw = payload.get('position')
                if not side_raw or not pos_raw: return None
                
                side = Side(side_raw)
                pos = Position.parse(pos_raw)
                if history_document.action_type == KingChecked.__name__:
                    event = KingChecked(game_id=game_id, side=side, position=pos)
                else:
                    event = KingCheckMated(game_id=game_id, side=side, position=pos)
            
            case KingCastledEvent.__name__:
                required_keys = ['side', 'king_from', 'king_to', 'rook_from', 'rook_to', 'is_kingside']
                if not all(k in payload for k in required_keys): return None

                event = KingCastledEvent(
                    game_id=game_id,
                    side=Side(payload['side']),
                    king_from=Position.parse(payload['king_from']),
                    king_to=Position.parse(payload['king_to']),
                    rook_from=Position.parse(payload['rook_from']),
                    rook_to=Position.parse(payload['rook_to']),
                    is_kingside=payload['is_kingside']
                )

        if event:
            return ChessGameHistoryEntry(
                entry_id=HistoryEntryId(PydanticObjectId(history_document.id)),
                sequence_number=history_document.sequence_number,
                history_event=event
            )
        return None

    @staticmethod
    async def create(game: ChessGame) -> list[GameHistoryDocument]:
        history_list: list[GameHistoryDocument] = list()
        game_id = game.game_id.value

        for history_entry in game.history:
            # Skip PieceMoveFailed as per user request
            if history_entry.action_type == PieceMoveFailed.__name__:
                continue

            history_document = GameHistoryDocument(
                _id=history_entry.id.value,
                game_id=game_id,
                sequence_number=history_entry.sequence_number,
                action_type=history_entry.action_type,
                action_date=datetime.datetime.now(),
                payload=domain_to_dict(history_entry.history_event)
            )
            history_list.append(history_document)

        return history_list