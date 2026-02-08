from aiokafka import AIOKafkaProducer
import json
from ...infrastructure.config.config import Settings


class KafkaProducerService:
    def __init__(self, settings: Settings):
        self._bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self._producer = None

    async def start(self):
        if not self._producer:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await self._producer.start()
        return self._producer

    async def stop(self):
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def send_message(self, topic: str, message: dict):
        producer = await self.start()
        await producer.send_and_wait(topic, message)
