from core.domain.kernel.entity import Entity


class ChessGameHistoryEntry(Entity):

    def __init__(self, sequence_number: int, history_event):
        super().__init__()
        self._seq_number = sequence_number
        self._history_event = history_event

    @property
    def sequence_number(self):
        return self._seq_number

    @property
    def history_event(self):
        return self._history_event

    @property
    def action_type(self):
        return self._history_event.__class__.__name__