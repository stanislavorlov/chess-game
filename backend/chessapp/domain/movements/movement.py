from ...domain.chessboard.position import Position

class Movement:

    def __init__(self, _from: Position, _to: Position):
        self._from = _from
        self._to = _to

    @property
    def from_position(self):
        return self._from

    @property
    def to_position(self):
        return self._to

    def to_string(self):
        return f'{str(self._from)} - {str(self._to)}'

    def __eq__(self, other):
        if isinstance(other, Movement):
            return (self._from == other._from and 
                    self._to == other._to)
        return False
        
    def to_dict(self):
        return {
            "from": str(self._from),
            "to": str(self._to)
        }

    def __hash__(self):
        return hash((self._from, self._to))