from Model.Board.chess_board import ChessBoard
from Model.Events.ChessGameDomainEvent import ChessGameDomainEvent
from Model.Events.DomainEventId import DomainEventId
from Model.Game.chess_game_id import ChessGameId
from Model.Pieces.Side import Side
from Model.Players.Players import Players

class ChessGameStartedData:
    
    def __init__(self, chessGameId: ChessGameId, chessBoard: ChessBoard, startSide: Side, players: Players):
        self._chessGameId = chessGameId
        self._chessBoard = chessBoard
        self._startSide = startSide
        self._players = players
        
class ChessGameStartedEvent(ChessGameDomainEvent):
    
    def __init__(self, gameId: ChessGameId, data: ChessGameStartedData):
        super().__init__(DomainEventId.generate_event_id())
        self._gameId = gameId
        self._data = data