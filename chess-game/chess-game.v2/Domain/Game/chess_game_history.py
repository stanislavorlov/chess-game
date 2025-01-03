from Model.Movements import MovementEvent

class ChessGameHistory:
    def __init__(self, history: []):
        self._gameHistory = history
        
    @staticmethod
    def get_empty() -> []:
        return []
    
    def record(self, entry: MovementEvent):
        self._gameHistory.append(entry)
        
    def last(self) -> MovementEvent:
        return self._gameHistory[-1]