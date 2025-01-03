from datetime import datetime
import uuid
from Model.Kernel.ValueObject import ValueObject

class DomainEventId(ValueObject):
    
    def __init__(self):
        self.event_id = self.generate_event_id()
        self.timestamp = datetime.utcnow()
        
    @staticmethod
    def generate_event_id():
        """
        Generate a unique identifier for the event using UUID4.
        """
        return str(uuid.uuid4())

    def __str__(self):
        """
        Return a string representation of the EventIdentifier.
        """
        return f"EventID: {self.event_id}, Timestamp: {self.timestamp.isoformat()}"