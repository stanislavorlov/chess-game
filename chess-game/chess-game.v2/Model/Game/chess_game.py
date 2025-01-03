from typing import List
from Model.Board.chess_board import ChessBoard
from Model.Events.ChessGameDomainEvent import ChessGameDomainEvent
from Model.Events.ChessGameStartedEvent import ChessGameStartedData, ChessGameStartedEvent
from Model.Game.chess_game_history import ChessGameHistory
from Model.Game.chess_game_id import ChessGameId
from Model.Game.chess_game_state import ChessGameState
from Model.Pieces.Side import Side
from Model.Players.Players import Players

class ChessGame(object):
    
    def __init__(self):
        self._history: ChessGameHistory = None
        self._state: ChessGameState = None
        self._domainEvents: List[ChessGameDomainEvent] = []
        
    def start(self, chessBoard: ChessBoard, id: ChessGameId, startSide: Side, players: Players):
        chessGameStartedData = ChessGameStartedData(id, chessBoard, startSide, players)
        chessGameStarted = ChessGameStartedEvent(id, chessGameStartedData)
        
        self._domainEvents.append(chessGameStarted)
        
        # ToDo: publish events to handler