"""
Restaurant endpoint
"""

from fastapi import APIRouter, status, Depends, Query
from uuid import UUID
from app.api.v1.schemas.restaurants import (
    CreateRestaurantRequest,
    CreateRestaurantResponse,
    GetAllRestrauntsRequest,
    GetAllRestrauntsResponse,
    UpdateRestaurantRequest,
    UpdateRestaurantResponse,
    GetRestaurantMenuRequest,
    GetRestaurantMenuResponse,
    GetRestaurantRequest,
    GetRestaurantResponse,
    ValidateOrderRequest,
    ValidateOrderResponse
)
from app.application.commands.create_restaurant import CreateRestaurantCommand, CreateRestaurantHandler
from app.application.commands.update_restaurant import UpdateRestaurantCommand, UpdateRestaurantHandler
from app.application.commands.validate_order import ValidateOrderCommand, ValidateOrderHandler, ValidateOrderResult
from app.application.queries.get_restraunts import GetAllRestrauntsQuery, GetAllRestrauntsHandler
from app.application.queries.get_restraunt_menu import GetRestaurantMenuQuery, GetRestaurantMenuHandler
from app.application.queries.get_restraunt import GetRestaurantQuery, GetRestaurantHandler
from app.api.dependencies.restaurants import (
    get_creating_restaurant_handler, 
    get_getting_all_restaurants_handler, 
    get_updating_restaurant_handler,
    get_restaurant_menu_getting_handler,
    get_restaurant_getting_handler,
    get_order_validating_handler
)

router = APIRouter(prefix="/restaurant", tags=["restaurants"])

@router.post("/", response_model=CreateRestaurantResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurant(request: CreateRestaurantRequest,
                            handler: CreateRestaurantHandler = Depends(get_creating_restaurant_handler)):
    
    command = CreateRestaurantCommand(name = request.name,
                                      city=request.address.city,
                                      street=request.address.street,
                                      house_number=request.address.house_number,
                                      building=request.address.building,
                                      floor=request.address.floor,
                                      contact_phone = request.contact_phone,
                                      working_schedule = request.schedule,
                                      is_active = request.is_active,
                                      description = request.description,
                                      coordinates = request.coordinates,
                                      tags = request.tags)
    
    result = await handler.handle(command)
    return CreateRestaurantResponse(
        id=result.get("id"),
        msg=result.get("msg")
    )

@router.get("/", response_model=GetAllRestrauntsResponse, status_code=status.HTTP_200_OK)
async def get_restraunts(
    request: GetAllRestrauntsRequest = Query(),
    handler: GetAllRestrauntsHandler = Depends(get_getting_all_restaurants_handler)
):
    command = GetAllRestrauntsQuery(
        page=request.page,
        per_page=request.per_page
    )

    result = await handler.handle(command)
    
    if result is None:
        raise

    return GetAllRestrauntsResponse(restraunts=result)

@router.get("/{id}", response_model=GetRestaurantResponse, status_code=status.HTTP_200_OK)
async def get_restraunt(
    request: GetRestaurantRequest = Query(),
    handler: GetRestaurantHandler = Depends(get_restaurant_getting_handler)
):
    command = GetRestaurantQuery(
        id=request.id
    )

    result = await handler.handle(command)
    
    if result is None:
        raise

    return GetRestaurantResponse(**result)

@router.patch("/", response_model=UpdateRestaurantResponse, status_code=status.HTTP_200_OK)
async def update_restaurant(
    request: UpdateRestaurantRequest,
    handler: UpdateRestaurantHandler = Depends(get_updating_restaurant_handler)
) -> UpdateRestaurantResponse:
    
    command = UpdateRestaurantCommand(
        id = request.id,
        name = request.name,
        city = request.address.city,
        street = request.address.street,
        house_number = request.address.house_number,
        building = request.address.building,
        floor = request.address.floor,
        contact_phone = request.contact_phone,
        schedule = request.schedule,
        is_active = request.is_active,
        description = request.description,
        coordinates = request.coordinates,
        tags = request.tags
    )

    result = await handler.handle(command)

    if result is None: 
        raise

    return UpdateRestaurantResponse(**result)

@router.get("/{restaurant_id}/menu", response_model=GetRestaurantMenuResponse, status_code=status.HTTP_200_OK)
async def get_restraunt_menu(
    request: GetRestaurantMenuRequest = Query(),
    handler: GetRestaurantMenuHandler = Depends(get_restaurant_menu_getting_handler)
) -> GetRestaurantMenuResponse:
    
    command = GetRestaurantMenuQuery(
        restaurant_id = request.restaurant_id
    )

    result = await handler.handle(command)
    
    if result is None:
        raise

    return GetRestaurantMenuResponse(menu=result)

@router.post("/{restaurant_id}/validate", response_model=ValidateOrderResponse, status_code=status.HTTP_200_OK)
async def validate_order(
    request: ValidateOrderRequest,
    restaurant_id: UUID,
    handler: ValidateOrderHandler = Depends(get_order_validating_handler)
) -> ValidateOrderResponse:
    
    items_as_dicts = [
        {
            "dish_id": item.dish_id,
            "quantity": item.quantity
        }
        for item in request.items
    ]
    
    command = ValidateOrderCommand(
        restaurant_id=restaurant_id,
        items=items_as_dicts
    )
    
    result = await handler.handle(command)
    return ValidateOrderResponse(
        is_valid=result.is_valid,
        validated_items=result.validated_items,
        errors=result.errors
    )