from fastapi import FastAPI
from app.api.v1.endpoints.auth import router as auth_router
from app.infrastructure.messaging.producer import KafkaEventProducer
from app.core.dependencies import  set_kafka_producer
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = KafkaEventProducer()
    try:
        await producer.start()
        set_kafka_producer(producer)
    except Exception as e:
        ...
    
    yield

    try:
        await producer.stop()
    except Exception as e:
        ...
    
app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1/auth")

@app.get("/")
async def root():
    return {"message": "Auth Service"}