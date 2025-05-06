from typing import Optional
from beanie import PydanticObjectId
from bson import ObjectId
from core.domain.kernel.value_object import ValueObject


class HistoryEntryId(ValueObject):

    def __init__(self, value: Optional[PydanticObjectId] = None):
        super().__init__()
        self._value = value

    @property
    def value(self) -> Optional[PydanticObjectId]:
        return self._value

    def __eq__(self, other):
        if isinstance(other, HistoryEntryId):
            return self._value == other._value
        return False

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f"ObjectId({self._value})"

    def __hash__(self):
        return hash(self._value)

    @staticmethod
    def empty():
        return HistoryEntryId(None)

    @staticmethod
    def generate_id():
        new_oid = ObjectId()
        pydantic_oid = PydanticObjectId(new_oid)

        return HistoryEntryId(pydantic_oid)