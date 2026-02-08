from ...domain.kernel.entity import Entity
from ...domain.value_objects.history_entry_id import HistoryEntryId


class ChessGameHistoryEntry(Entity):

    def __init__(self, entry_id: HistoryEntryId, sequence_number: int, history_event):
        super().__init__()
        self._id = entry_id
        self._seq_number = sequence_number
        self._history_event = history_event

    @property
    def id(self) -> HistoryEntryId:
        return self._id

    @property
    def sequence_number(self):
        return self._seq_number

    @property
    def history_event(self):
        return self._history_event

    @property
    def action_type(self):
        return self._history_event.__class__.__name__