from fastapi import FastAPI
from app.api.v1.endpoints.users import router as user_router

app = FastAPI()
app.include_router(user_router, prefix="/api/v1/user")

@app.get("/")
async def root():
    return {"message": "User Service"}