import re
from datetime import datetime
from ...application.dtos.chess_game_dto import ChessGameDto, GameStateDto, GameFormatDto, PlayersDto
from ...domain.chessboard.board import Board
from ...domain.events import (
    GameCreated, KingCastled,
    PawnPromoted, PieceCaptured,
    PieceMoved
)
from ...domain.game import ChessGame, ChessGameHistory
from ...domain.movements.movement import Movement
from ...domain.pieces import King, Piece
from ...domain.value_objects import SAN, Side
from ...domain.services.fen_service import FenService
from ...domain.services.san_service import SanService


class DtoMapper:

    @staticmethod
    def map_game(game: ChessGame) -> ChessGameDto:
        return ChessGameDto(
            game_id=str(game.game_id),
            moves_count=game.history.moves_count(),
            date=game.information.date,
            name=game.information.name,
            status=str(game.game_state.status),
            state=DtoMapper._map_component(game.game_state),
            game_format=DtoMapper._map_game_format(game.information.format, game),
            players=DtoMapper._map_component(game.players),
            board=FenService.generate(game.get_board()),
            history=DtoMapper.map_history(game.history),
        )

    @staticmethod
    def _map_component(component: any) -> any:
        component_name = DtoMapper._to_snake_case(component.__class__.__name__)
        mapper_name = f"_map_{component_name}"
        mapper = getattr(DtoMapper, mapper_name, None)
        
        if mapper and callable(mapper):
            return mapper(component)
        
        return component

    @staticmethod
    def _to_snake_case(name: str) -> str:
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def _map_game_state(state: any) -> GameStateDto:
        check_side = state.check_state.side_checked.value() if state.check_state.side_checked else None
        check_pos = str(state.check_state.position_checked) if state.check_state.position_checked else None
        
        legal_moves = ""
        if state.is_started and not state.is_finished:
            # Compact UCI format: "e2e4 e7e5"
            moves : list[Movement] = state.board.get_legal_moves(state.turn)
            legal_moves = " ".join([str(m.to_uci()) for m in moves])

        return GameStateDto(
            turn=state.turn.value(),
            started=state.is_started,
            finished=state.is_finished,
            check_side=check_side,
            check_position=check_pos,
            legal_moves=legal_moves
        )

    @staticmethod
    def _map_game_format(game_format: any, game: ChessGame) -> GameFormatDto:
        white_remaining = game.white_timer
        black_remaining = game.black_timer
        
        if game.game_state.is_started and not game.game_state.is_finished:
            last_event = game.history.last()
            # If no history yet, use game start date
            last_date = last_event.action_date if last_event else game.game_state.started_at
            
            if last_date:
                elapsed = (datetime.now() - last_date).total_seconds()
                if game.game_state.turn == Side.white():
                    white_remaining -= elapsed
                else:
                    black_remaining -= elapsed

        return GameFormatDto(
            value=game_format.to_string(),
            white_remaining_time=max(0, white_remaining),
            black_remaining_time=max(0, black_remaining),
            move_increment=game_format.time_remaining.move_increment.total_seconds(),
        )

    @staticmethod
    def _map_players(players: any) -> PlayersDto:
        return PlayersDto(
            white_id=str(players.white),
            black_id=str(players.black)
        )

    @staticmethod
    def map_history(history: ChessGameHistory) -> str:
        sans = []
        board = Board()
        
        allowed_events = [PieceMoved.__name__, KingCastled.__name__, PieceCaptured.__name__, PawnPromoted.__name__]

        for item in history:
            event = item.history_event
            class_name = item.action_type
            
            board_before = board.clone()
            
            if class_name == PieceMoved.__name__:
                board.piece_moved(event)
            elif class_name == PieceCaptured.__name__:
                board.piece_captured(event)
            elif class_name == KingCastled.__name__:
                board.king_castled(event)
            elif class_name == PawnPromoted.__name__:
                board.pawn_promoted(event)
            elif class_name == GameCreated.__name__:
                board = Board() 

            if class_name not in allowed_events:
                continue

            if event.has_san:
                san = SanService.calculate(event, board_before)
                sans.append(str(san))

        return ",".join(sans)

    @staticmethod
    def _map_piece_moved(event: PieceMoved) -> dict:
        return {
            'piece': DtoMapper.map_piece(event.piece),
            'from': str(event.from_),
            'to': str(event.to),
            'type': 'move'
        }

    @staticmethod
    def _map_king_castled(event: KingCastled) -> dict:
        return {
            'piece': DtoMapper.map_piece(King(event.side)),
            'from': 'O',
            'to': 'O' if event.is_kingside else 'O-O',
            'type': 'castling'
        }

    @staticmethod
    def map_board(board: Board) -> list:
        output = []

        for position in board:
            square = board[position]
            output.append({
                'square': str(square.position),
                'piece': DtoMapper.map_piece(square.piece),
                'color': str(square.color),
                'rank': square.position.rank.value
            })

        return output

    @staticmethod
    def map_piece(piece: Piece):
        if piece:
            return {
                'abbreviation': piece.get_abbreviation(),
                'moved': piece.is_moved
            }

        return None