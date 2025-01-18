from domain.chessboard.chess_board import ChessBoard
from domain.chessboard.position import Position
from domain.side import Side
from domain.pieces.bishop import Bishop
from domain.pieces.king import King
from domain.pieces.knight import Knight
from domain.pieces.pawn import Pawn
from domain.pieces.queen import Queen
from domain.pieces.rook import Rook

class GameState(object):
    
    def __init__(self, player_side: Side, board: ChessBoard):
        self._playerSide = player_side
        self._state = []
        self._board = board
        self.__initialize_game(self._playerSide)

    def __initialize_game(self, player_side: Side):
        state = [
            [Rook(Side.black()), Knight(Side.black()), Bishop(Side.black()), Queen(Side.black()), King(Side.black()), Bishop(Side.black()), Knight(Side.black()), Rook(Side.black())],
            [Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black())],
            [ None, None, None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None],
            [Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white())],
            [Rook(Side.white()), Knight(Side.white()), Bishop(Side.white()), Queen(Side.white()), King(Side.white()), Bishop(Side.white()), Knight(Side.white()), Rook(Side.white())],
        ]

        game_state = {}

        # ToDo: hashtable of positions and pieces (i.e. { 'e2': Pawn(Side.white() } })
        
        if str(player_side) == str(Side.black()):
            state.reverse()

        positional_state = {}
        for rank in range(len(state)):
            for file in range(len(state[rank])):
                game_state[str(self._board.get_position_by_file_rank_idx(file, rank))] = state[file][rank]

        self._state = state
        
    def get_state(self):
        return self._state