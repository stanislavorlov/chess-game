from core.application.handlers.base_handler import BaseHandler
from core.domain.events.movement_started import MovementStarted


class MovementStartedHandler(BaseHandler[MovementStarted]):

    def handle(self, event: MovementStarted):
        pass