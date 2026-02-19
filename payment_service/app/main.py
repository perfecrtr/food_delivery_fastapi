

import asyncio
import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from aiokafka import AIOKafkaProducer

from app.core.config import settings
from app.infrastructure.db.database import AsyncSessionLocal, get_db
from app.infrastructure.db.repositories.payment_repository import SQLAlchemyPaymentRepository
from app.infrastructure.gateway.mock_payment_gateway import MockPaymentGatewayAdapter
from app.application.handlers.order_events import OrderEventsHandler
from app.infrastructure.messaging.consumer import KafkaEventConsumer
from app.infrastructure.messaging.producer import KafkaEventProducer
from app.core.dependencies import get_event_producer


@asynccontextmanager
async def lifespan(app: FastAPI):

    db_session: AsyncSession = AsyncSessionLocal()
    payment_repo = SQLAlchemyPaymentRepository(db=db_session)
    payment_gateway = MockPaymentGatewayAdapter()
    kafka_producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        client_id=settings.kafka_client_id
    )
    await kafka_producer.start()

    event_producer = KafkaEventProducer(kafka_producer)

    app.state.db_session = db_session
    app.state.payment_repo = payment_repo
    app.state.payment_gateway = payment_gateway
    app.state.kafka_producer = kafka_producer
    app.state.event_producer = event_producer

    order_events_handler = OrderEventsHandler(payment_repo, payment_gateway, event_producer=event_producer)
    kafka_consumer = KafkaEventConsumer(order_events_handler=order_events_handler)

    app.state.order_events_handler = order_events_handler
    app.state.kafka_consumer = kafka_consumer

    consumer_task = asyncio.create_task(kafka_consumer.run_forever())
    app.state.kafka_task = consumer_task

    try:
        yield
    finally:
        await kafka_producer.stop()
        await kafka_consumer.stop()
        consumer_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await consumer_task
        await db_session.close()


app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "Payment Service"}