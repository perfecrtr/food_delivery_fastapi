from fastapi import FastAPI
from app.api.v1.endpoints.orders import router as order_router
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer

from app.core.config import settings

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
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        client_id=settings.KAFKA_CLIENT_ID
    )

    await producer.start()
    app.state.kafka_producer = producer
    try:
        yield
    finally:
        await producer.stop()

app = FastAPI(lifespan=lifespan)

app.openapi = custom_openapi

app.include_router(order_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Order Service"}