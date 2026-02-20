import re
from ...application.dtos.chess_game_dto import ChessGameDto, GameStateDto, GameFormatDto, PlayersDto
from ...domain.chessboard.board import Board
from ...domain.events.king_castled import KingCastled
from ...domain.events.piece_moved import PieceMoved
from ...domain.game.chess_game import ChessGame
from ...domain.game.game_history import ChessGameHistory
from ...domain.pieces.king import King
from ...domain.pieces.piece import Piece


class DtoMapper:

    @staticmethod
    def map_game(game: ChessGame) -> ChessGameDto:
        return ChessGameDto(
            game_id=str(game.game_id),
            date=game.information.date,
            name=game.information.name,
            status=str(game.game_state.status),
            state=DtoMapper._map_component(game.game_state),
            game_format=DtoMapper._map_component(game.information.format),
            players=DtoMapper._map_component(game.players),
            board=DtoMapper.map_board(game.get_board()),
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

        return GameStateDto(
            turn=state.turn.value(),
            started=state.is_started,
            finished=state.is_finished,
            check_side=check_side,
            check_position=check_pos
        )

    @staticmethod
    def _map_game_format(game_format: any) -> GameFormatDto:
        return GameFormatDto(
            value=game_format.to_string(),
            remaining_time=game_format.time_remaining.main_time.total_seconds(),
            additional_time=game_format.time_remaining.additional_time.total_seconds(),
        )

    @staticmethod
    def _map_players(players: any) -> PlayersDto:
        return PlayersDto(
            white_id=str(players.white),
            black_id=str(players.black)
        )

    @staticmethod
    def map_history(history: ChessGameHistory) -> list:
        output = []
        allowed_events = [PieceMoved.__name__, KingCastled.__name__]

        for item in history:
            event = item.history_event
            class_name = item.action_type
            
            if class_name not in allowed_events:
                continue

            event_name = DtoMapper._to_snake_case(class_name)
            mapper_name = f"_map_{event_name}"
            mapper = getattr(DtoMapper, mapper_name, None)
            
            if mapper and callable(mapper):
                event_data = mapper(event)
                if isinstance(event_data, dict):
                    event_data.update({
                        'sequence': item.sequence_number,
                        'action_type': item.action_type
                    })
                output.append(event_data)

        return output

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