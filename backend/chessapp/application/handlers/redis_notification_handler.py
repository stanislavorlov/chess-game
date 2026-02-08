import json
from ...application.handlers.base_event_handler import BaseEventHandler
from ...domain.kernel.base import BaseEvent
from ...infrastructure.services.redis_service import RedisService


class RedisNotificationHandler(BaseEventHandler[BaseEvent, None]):
    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service

    async def handle(self, event: BaseEvent) -> None:
        # Most events have a game_id, but we use a fallback channel if missing
        game_id = getattr(event, 'game_id', None)
        
        if game_id:
            channel = f"chess-notifications:{game_id}"
        else:
            channel = "chess-notifications:global"

        message = json.dumps(event.to_dict(), default=str)
        await self.redis_service.publish(channel, message)
