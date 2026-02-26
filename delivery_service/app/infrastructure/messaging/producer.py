from aiokafka import AIOKafkaProducer
from typing import Any
import json

from app.domain.services.event_producer import EventProducer, DomainEvent
from app.core.config import settings

class KafkaEventProducer(EventProducer):

    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer
    
    async def publish(self, topic: str, event: DomainEvent) -> None:
        payload: dict[str, Any] = event.__dict__

        value = json.dumps(payload, default=str).encode("utf-8")
        await self._producer.send_and_wait(topic=topic, value=value)