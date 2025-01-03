from typing import List
from Model.Events.ChessGameDomainEvent import ChessGameDomainEvent
from Model.Game.chess_game_history import ChessGameHistory
from Model.Game.chess_game_state import ChessGameState

class ChessGame(object):
    
    def __init__(self):
        self._history: ChessGameHistory = None
        self._state: ChessGameState = None
        self._domainEvents: List[ChessGameDomainEvent] = []
        
    


