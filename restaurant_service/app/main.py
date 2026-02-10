from fastapi import FastAPI
from app.api.v1.endpoints.restaurants import router as restraunt_router
from app.api.v1.endpoints.menu_categories import router as menu_category_router
from app.api.v1.endpoints.dishes import router as dish_router


app = FastAPI()

app.include_router(restraunt_router, prefix="/api/v1/restraunt")
app.include_router(menu_category_router, prefix="/api/v1/restraunt")
app.include_router(dish_router, prefix="/api/v1/restraunt")

@app.get("/")
async def root():
    return {"message": "Restaurant Service"}