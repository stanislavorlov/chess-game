class Delta:

    def __init__(self, delta: int):
        self._delta = abs(delta)

    def has_changed(self):
        return self._delta != 0

    def __eq__(self, other):
        if not isinstance(other, Delta):
            return False

        return self._delta == other._delta or other._delta == Delta.any()._delta

    @staticmethod
    def zero():
        return Delta(0)

    @staticmethod
    def one():
        return Delta(1)

    @staticmethod
    def any():
        return Delta(100)

    def __str__(self):
        return str(self._delta)