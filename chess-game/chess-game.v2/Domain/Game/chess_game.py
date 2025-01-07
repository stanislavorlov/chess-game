from typing import List

from Domain.Board.chess_board import ChessBoard
from Domain.Events.ChessGameDomainEvent import ChessGameDomainEvent
from Domain.Events.ChessGameStartedEvent import ChessGameStartedData, ChessGameStartedEvent
from Domain.Game.chess_game_history import ChessGameHistory
from Domain.Game.chess_game_id import ChessGameId
from Domain.Game.chess_game_state import ChessGameState
from Domain.Pieces.Side import Side
from Domain.Players.Players import Players
from Infrastructure.mediator import Mediator

class ChessGame(object):
    
    def __init__(self, mediator: Mediator):
        self._history: ChessGameHistory = None
        self._state: ChessGameState = None
        self._mediator = mediator
        
    def start(self, chessBoard: ChessBoard, id: ChessGameId, startSide: Side, players: Players):
        chessGameStartedData = ChessGameStartedData(id, chessBoard, startSide, players)
        chessGameStarted = ChessGameStartedEvent(id, chessGameStartedData)
        
        self._mediator.publish(chessGameStarted)