from application.handlers.base_handler import BaseHandler, T
from domain.events.movement_completed import MovementCompleted


class MovementCompletedHandler(BaseHandler[MovementCompleted]):

    def handle(self, event: MovementCompleted):
        pass