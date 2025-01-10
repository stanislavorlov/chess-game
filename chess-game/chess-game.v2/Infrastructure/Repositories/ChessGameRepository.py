from typing import Optional
from Domain.Game.chess_game import ChessGame
from Domain.Game.chess_game_id import ChessGameId

class ChessGameRepository:
    
    def __init__(self):
        self._games = {}
        
    def start_game(self, id: ChessGameId, game: ChessGame):
        self._games[id] = game
        
    def get_game(self, id: ChessGameId) -> Optional[ChessGame]:
        if id in self._games:
            return self._games[id]
        
        return None