from calendar import c
from Domain.Events.ChessGameStartedEvent import ChessGameStartedEvent
from Domain.Game.chess_game import ChessGame
from Infrastructure.Repositories.ChessGameRepository import ChessGameRepository

class ChessGameStartedHandler:
    
    def __init__(self, repository: ChessGameRepository):
        self._repository = repository
        
    def handle(self, command : ChessGameStartedEvent):
        chessGameId = command._data._chessGameId
        
        chessGame = self._repository.get_game(chessGameId)

        if not chessGame:
            chessGame = ChessGame()
            
        chessGame._state._started = True
        chessGame._state._finished = False
        chessGame._state._board = command._data._chessBoard
        chessGame._state._id = chessGameId
        chessGame._state._players = command._data._players
        
        self._repository.start_game(chessGameId, chessGame)