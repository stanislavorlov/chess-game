class GameFormat:

    def __init__(self, time_minutes: int):
        self._time_minutes = time_minutes

    @staticmethod
    def rapid():
        return GameFormat(10)

    @staticmethod
    def blitz():
        return GameFormat(5)

    @staticmethod
    def bullet():
        return GameFormat(1)

    def extend(self):
        pass
