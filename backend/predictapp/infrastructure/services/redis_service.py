import redis.asyncio as redis
from ...infrastructure.config.config import Settings


class RedisService:
    def __init__(self, settings: Settings):
        self._url = settings.REDIS_URL
        self._redis = None

    async def connect(self):
        if not self._redis:
            self._redis = redis.from_url(self._url, decode_responses=True)
        return self._redis

    async def publish(self, channel: str, message: str):
        r = await self.connect()
        await r.publish(channel, message)

    async def subscribe(self, channel_pattern: str):
        r = await self.connect()
        pubsub = r.pubsub()
        if '*' in channel_pattern:
            await pubsub.psubscribe(channel_pattern)
        else:
            await pubsub.subscribe(channel_pattern)
        
        try:
            async for message in pubsub.listen():
                if message['type'] in ('message', 'pmessage'):
                    yield message['data']
        finally:
            await pubsub.close()

    async def disconnect(self):
        if self._redis:
            await self._redis.close()
            self._redis = None
