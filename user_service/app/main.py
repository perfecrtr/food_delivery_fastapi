from fastapi import FastAPI
import asyncio
from app.api.v1.endpoints.users import router as user_router
from app.infrastructure.messaging.consumer import kafka_consumer
from app.application.handlers.user_events import UserEventsHandler
from app.core.config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    events_handler = UserEventsHandler()
    kafka_consumer.register_handler(
        settings.KAFKA_TOPIC_USER_REGISTERED,
        events_handler.handle_user_registered 
    )
    await kafka_consumer.connect()
    consumer_task = asyncio.create_task(kafka_consumer.consume())
    yield
    await kafka_consumer.close()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/api/v1/user")

@app.get("/")
async def root():
    return {"message": "User Service"}