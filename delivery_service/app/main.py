from fastapi import FastAPI
from app.api.v1.endpoints.couriers import router as courier_router
from app.api.v1.endpoints.deliveries import router as delivery_router
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import contextlib
from aiokafka import AIOKafkaProducer

from app.infrastructure.db.database import  AsyncSessionLocal
from app.infrastructure.db.repositories.delivery_repository import SQLAlchemyDeliveryRepository
from app.infrastructure.db.repositories.courier_repository import SQLAlchemyCourierRepository
from app.infrastructure.messaging.consumer import KafkaEventConsumer
from app.application.handlers.order_events import OrderEventsHandler
from app.infrastructure.services.courier_assignment import SimpleRandomCourierAssignment
from app.infrastructure.messaging.producer import KafkaEventProducer
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):

    db_session: AsyncSession = AsyncSessionLocal()
    delivery_repo = SQLAlchemyDeliveryRepository(db=db_session)
    courier_repo = SQLAlchemyCourierRepository(db=db_session)
    courier_assigner = SimpleRandomCourierAssignment(courier_repo=courier_repo, delivery_repo=delivery_repo)
    kafka_producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        client_id=settings.kafka_client_id,
    )

    await kafka_producer.start()
    event_producer = KafkaEventProducer(kafka_producer)

    app.state.db_session = db_session
    app.state.delivery_repo = delivery_repo
    app.state.courier_repo = courier_repo
    app.state.courier_assigner = courier_assigner
    app.state.event_producer = event_producer

    order_events_handler = OrderEventsHandler(delivery_repo=delivery_repo, courier_repo=courier_repo, courier_assigner=courier_assigner)
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
app.include_router(courier_router, prefix="/api/v1")
app.include_router(delivery_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Delivery Service"}