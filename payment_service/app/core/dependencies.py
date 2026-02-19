from fastapi import Request

from app.domain.services.event_producer import EventProducer
from app.infrastructure.messaging.producer import KafkaEventProducer


async def get_event_producer(request: Request) -> EventProducer:
    kafka_producer = request.app.state.kafka_producer
    return KafkaEventProducer(producer=kafka_producer)