from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
import asyncio
from ...infrastructure.config.config import Settings


class KafkaService:
    def __init__(self, settings: Settings):
        self._bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self._producer = None
        self._consumers = {}

    async def start_producer(self):
        if not self._producer:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await self._producer.start()
        return self._producer

    async def stop_producer(self):
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def send_message(self, topic: str, message: dict):
        producer = await self.start_producer()
        await producer.send_and_wait(topic, message)

    async def consume_messages(self, topic: str, group_id: str = None):
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self._bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        await consumer.start()
        try:
            async for msg in consumer:
                yield msg.value
        finally:
            await consumer.stop()

    async def stop_all(self):
        await self.stop_producer()
        # Consumers are managed via the generator's finally block
