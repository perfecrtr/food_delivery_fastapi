from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.endpoints.orders import router as order_router
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import contextlib
import asyncio

from aiokafka import AIOKafkaProducer

from app.core.config import settings
from app.infrastructure.db.database import AsyncSessionLocal
from app.infrastructure.db.repositories.order_repository import SQLAlchemyOrderRepository
from app.infrastructure.messaging.producer import KafkaEventProducer
from app.infrastructure.messaging.consumer import KafkaEventConsumer
from app.application.handlers.payment_events import PaymentEventsHandler
from app.application.handlers.delivery_events import DeliveryEventsHandler

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Order Service API",
        version="1.0.0",
        description="API для управления заказами",
        routes=app.routes,
    )
    
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if operation.get("operationId", "").startswith("create") or operation.get("summary", "").lower().find("create") != -1:
                if "parameters" not in operation:
                    operation["parameters"] = []
                operation["parameters"].append({
                    "name": "Idempotency-Key",
                    "in": "header",
                    "required": True,
                    "schema": {
                        "type": "string",
                        "format": "uuid",
                        "example": "123e4567-e89b-12d3-a456-426614174000"
                    },
                    "description": "Уникальный ключ идемпотентности (UUID v4)"
                })
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@asynccontextmanager
async def lifespan(app: FastAPI):

    db_session: AsyncSession = AsyncSessionLocal()
    order_repo = SQLAlchemyOrderRepository(db=db_session)
    kafka_producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        client_id=settings.KAFKA_CLIENT_ID
    )

    await kafka_producer.start()

    event_producer = KafkaEventProducer(kafka_producer)

    app.state.db_session = db_session
    app.state.order_repo = order_repo
    app.state.kafka_producer = kafka_producer
    app.state.event_producer = event_producer

    payment_events_handler = PaymentEventsHandler(order_repo, event_producer=event_producer)
    delivery_events_handler = DeliveryEventsHandler(repo=order_repo)
    kafka_consumer = KafkaEventConsumer(payment_events_handler=payment_events_handler, delivery_events_handler=delivery_events_handler)

    app.state.payment_events_handler = payment_events_handler
    app.state.delivery_events_handler = delivery_events_handler
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

app.openapi = custom_openapi

app.include_router(order_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Order Service"}