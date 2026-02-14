import dataclasses
from enum import Enum
from typing import Any


def domain_to_dict(obj: Any) -> Any:
    """
    Recursively converts domain objects (dataclasses, objects with to_dict, 
    enums, lists, dicts) into a JSON-serializable dictionary.
    """
    if dataclasses.is_dataclass(obj):
        result = {}
        for f in dataclasses.fields(obj):
            value = getattr(obj, f.name)
            result[f.name] = domain_to_dict(value)
        return result
    
    if isinstance(obj, list):
        return [domain_to_dict(i) for i in obj]
    
    if isinstance(obj, dict):
        return {str(k): domain_to_dict(v) for k, v in obj.items()}
    
    if isinstance(obj, Enum):
        return obj.value

    # Handle custom domain objects that aren't dataclasses
    if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')) and not isinstance(obj, type):
        # Avoid infinite recursion if to_dict calls domain_to_dict
        return obj.to_dict()

    # Specific handling for common custom domain objects if they don't have to_dict
    from ...domain.chessboard.position import Position
    if isinstance(obj, Position):
        return str(obj)

    from ...domain.value_objects.side import Side
    if isinstance(obj, Side):
        return obj.value()

    from ...domain.value_objects.game_id import ChessGameId
    if isinstance(obj, ChessGameId):
        return str(obj.value)

    from ...domain.pieces.piece import Piece
    if isinstance(obj, Piece):
        return {
            "piece_id": str(obj.get_piece_id().value),
            "side": obj.get_side().value(),
            "type": obj.get_piece_type(),
            "abbreviation": obj.get_abbreviation()
        }

    # Fallback to string representation for unknown objects (like ObjectIds)
    if hasattr(obj, '__str__'):
        # Check if it's a basic type first
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        return str(obj)

    return obj
