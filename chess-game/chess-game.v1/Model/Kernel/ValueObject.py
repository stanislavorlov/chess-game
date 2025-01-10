class ValueObject(object):
    
    def __init__(self) -> None:
        pass

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ValueObject):
            return False
        
        return True