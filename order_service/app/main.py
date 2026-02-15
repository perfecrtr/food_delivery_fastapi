from fastapi import FastAPI
from app.api.v1.endpoints.orders import router as order_router


app = FastAPI()

app.include_router(order_router, prefix="/api/v1/order")

@app.get("/")
async def root():
    return {"message": "Order Service"}