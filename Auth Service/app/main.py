from fastapi import FastAPI
from app.api.v1.endpoints.auth import router as auth_router
from app.infrastructure.messaging.producer import kafka_event_producer
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_event_producer.start()
    yield
    await kafka_event_producer.stop()

    
app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1/auth")

@app.get("/")
async def root():
    return {"message": "Auth Service"}