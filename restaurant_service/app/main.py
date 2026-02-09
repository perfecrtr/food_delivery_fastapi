from fastapi import FastAPI
from app.api.v1.endpoints.restaurants import router as restraunt_router


app = FastAPI()

app.include_router(restraunt_router, prefix="/api/v1/restraunt")

@app.get("/")
async def root():
    return {"message": "Restaurant Service"}