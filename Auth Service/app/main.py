from fastapi import FastAPI
from app.api.v1.endpoints.auth import router as auth_router
from contextlib import asynccontextmanager

app = FastAPI()
app.include_router(auth_router, prefix="/api/v1/auth")

@app.get("/")
async def root():
    return {"message": "Auth Service"}