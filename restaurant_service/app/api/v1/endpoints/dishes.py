from fastapi import APIRouter, status, Depends
from app.api.v1.schemas.dishes import (
    CreateDishRequest,
    CreateDishResponse,
    UpdateDishRequest,
    UpdateDishResponse
)
from app.application.commands.create_dish import CreateDishCommand, CreateDishHandler
from app.application.commands.update_dish import UpdateDishCommand, UpdateDishHandler
from app.api.dependencies.dishes import(
    get_dish_creating_handler,
    get_dish_updating_handler
)

router = APIRouter(prefix="/dishes", tags=["dishes"])

@router.post("/", response_model=CreateDishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(
    request: CreateDishRequest,
    handler: CreateDishHandler = Depends(get_dish_creating_handler)
) -> CreateDishResponse:
    
    command = CreateDishCommand(
        restaurant_id=request.restaurant_id,
        price=request.price,
        name=request.name,
        category_id=request.category_id,
        description=request.description,
        weight=request.weight,
        is_available=request.is_available
    )

    result = await handler.handle(command)

    return CreateDishResponse(**result)

@router.patch("/", response_model=UpdateDishResponse, status_code=status.HTTP_200_OK)
async def update_dish(
    request: UpdateDishRequest,
    handler: UpdateDishHandler = Depends(get_dish_updating_handler)
) -> UpdateDishResponse:
    
    command = UpdateDishCommand(
        id = request.id,
        restaurant_id=request.restaurant_id,
        price=request.price,
        name=request.name,
        category_id=request.category_id,
        description=request.description,
        weight=request.weight,
        is_available=request.is_available
    )

    result = await handler.handle(command)

    if result is None: 
        raise

    return UpdateDishResponse(**result)