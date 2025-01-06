from Domain.Board.chess_board import ChessBoard
from Domain.Events.ChessGameDomainEvent import ChessGameDomainEvent
from Domain.Events.DomainEventId import DomainEventId
from Domain.Game.chess_game_id import ChessGameId
from Domain.Pieces.Side import Side
from Domain.Players.Players import Players

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