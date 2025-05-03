from core.domain.chessboard.position import Position
from core.domain.events.game_created import GameCreated
from core.domain.events.game_start_failed import GameStartFailed
from core.domain.events.game_started import GameStartedEvent
from core.domain.events.piece_move_failed import PieceMoveFailed
from core.domain.events.piece_moved import PieceMoved
from core.domain.events.piece_moved_completed import PieceMovedCompleted
from core.domain.game.game_history import ChessGameHistory
from core.domain.kernel.aggregate_root import AggregateRoot
from core.domain.players.player_id import PlayerId
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.game_information import GameInformation
from core.domain.value_objects.game_state import GameState
from core.domain.value_objects.game_status import GameStatus
from core.domain.value_objects.side import Side


class ChessGame(AggregateRoot):

    def __init__(self, game_id: ChessGameId, game_info: GameInformation,
                 state: GameState, players: Players, history: ChessGameHistory):
        super().__init__()
        self._id = game_id
        self._info = game_info
        self._state = state
        self._players = players

        self._history = history

    @staticmethod
    def create(game_id: ChessGameId, game_info: GameInformation, players: Players):
        history = ChessGameHistory.empty()
        history.record(GameCreated(game_id=game_id))

        chess_game = ChessGame(game_id, game_info,
                               GameState(GameStatus.created(), Side.white()),
                               players, history)

        chess_game.raise_event(GameCreated(game_id=chess_game.game_id))

        return chess_game

    @property
    def information(self):
        return self._info

    @property
    def game_id(self):
        return self._id

    @property
    def game_state(self):
        return self._state

    @property
    def players(self):
        return self._players

    @property
    def history(self):
        return self._history

    def start(self):
        if self._state.is_started:
            return self.raise_event(GameStartFailed(game_id=self.game_id))
        else:
            self._state.update_status(GameStatus.started())

            return self.raise_event(GameStartedEvent(game_id=self.game_id))

    def move_piece(self, player_id: PlayerId, _from: Position, to: Position):
        self._history.record(PieceMovedCompleted(game_id=self.game_id,from_=_from,to=to))

        # if not self._state.is_started:
        #     return self.raise_event(PieceMoveFailed(from_=_from, to=to, reason='Game was not started', piece=None))
        # elif self._state.is_finished:
        #     return self.raise_event(PieceMoveFailed(from_=_from, to=to, reason='Game has finished'))
        #
        # piece = self._board.get_piece(_from)
        # if PlayerId(piece.get_side()) != player_id:
        #     return self.raise_event(PieceMoveFailed(from_=_from, to=to, reason="Piece doesn't belong to player"))
        #
        # if PlayerId(self._state.turn) != player_id:
        #     return self.raise_event(PieceMoveFailed(from_=_from, to=to,
        #                                                reason=f"It is not order of {player_id} player"))


    def calculate_move_effect(self):
        pass
        # promotion happened
        # piece captured
        # king check
        # checkmate
        # stalemate

        # publish event

    def promote_pawn(self):
        pass

    def __record_to_history(self):
        pass


    # def __init__2(self, state: GameState, presenter: AbstractPresenter, specification: MovementSpecification):
    #     # ToDo: generic unique ID of the game
    #
    #     self._started : bool = False
    #     self._finished : bool = False
    #     self._selectedPiece: Optional[Piece] = None
    #     self._fromPosition: Optional[Position] = None
    #     self._toPosition: Optional[Position] = None
    #     self._gameState: GameState = state
    #     self._presenter: AbstractPresenter = presenter
    #     self._moveSpecification: MovementSpecification = specification
    #     self._timer = Timer(60.0 * 10, self.stop)
    #
    #     self._presenter.onclick_handler(callback=self.make_action)
    #
    # def start(self, player_side: Side):
    #     self._started = True
    #     self._gameState.init(player_side)
    #     self._presenter.draw(self._gameState)
    #     self._timer.start()
    #
    # def make_action(self, position: Position):
    #     selected_piece = self._gameState.select_piece(position)
    #
    #     if (not self._selectedPiece) or (selected_piece and selected_piece.get_side() == self._selectedPiece.get_side()):
    #         self.select_piece(selected_piece, position)
    #     else:
    #         self._toPosition = position
    #         movement: Movement = Movement(self._selectedPiece, self._fromPosition, self._toPosition)
    #         if self._moveSpecification.is_satisfied_by(movement):
    #             self._gameState.move_piece(movement)
    #             self._selectedPiece = None
    #             self._presenter.draw(self._gameState)
    #         else:
    #             print('invalid movement')
    #
    #     # ToDo: return action instead: MOVE, SELECT, TAKE, CASTLING, CHECK, CHECKMATE, PROMOTE
    #
    # def select_piece(self, piece: Piece, position: Position):
    #     self._selectedPiece = piece
    #     self._fromPosition = position
    #
    # def stop(self):
    #     print('end game')