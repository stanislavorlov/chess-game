from core.application.dtos.chess_game_dto import ChessGameDto, GameStateDto, GameFormatDto, PlayersDto
from core.domain.chessboard.board import Board
from core.domain.chessboard.square import Square
from core.domain.game.chess_game import ChessGame
from core.domain.game.game_history import ChessGameHistory


class DtoMapper:

    @staticmethod
    def map_game(game: ChessGame) -> ChessGameDto:
        state_result = GameStateDto(
            turn=game.game_state.turn.value(),
            started=game.game_state.is_started,
            finished=game.game_state.is_finished
        )

        format_result = GameFormatDto(
            value=game.information.format.to_string(),
            remaining_time=game.information.format.time_remaining.main_time,
            additional_time=game.information.format.time_remaining.additional_time,
        )

        players_result = PlayersDto(
            white_id=str(game.players.white),
            black_id=str(game.players.black)
        )

        board = Board(game)

        return ChessGameDto(
            game_id=str(game.game_id),
            date=game.information.date,
            name=game.information.name,
            state=state_result,
            game_format=format_result,
            players=players_result,
            board=DtoMapper.map_board(board),
            history=DtoMapper.map_history(game.history),
        )

    @staticmethod
    def map_history(history: ChessGameHistory) -> list:
        output = []

        for item in history:
            pass

        return output

    @staticmethod
    def map_board(board: Board) -> list:
        output = []

        for position in board:
            square = board[position]
            output.append({
                'square': str(square.position),
                'piece': DtoMapper.map_square(square),
                'color': str(square.color),
                'rank': square.position.rank.value
            })

        return output

    @staticmethod
    def map_square(square: Square):
        if square.piece:
            return {
                'piece_id': square.piece.get_piece_id().value,
                'abbreviation': square.piece.get_abbreviation()
            }

        return None