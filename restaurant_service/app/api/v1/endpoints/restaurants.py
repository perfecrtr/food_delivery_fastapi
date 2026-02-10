"""
Restaurant endpoint
"""

from fastapi import APIRouter, status, Depends, Query
from app.api.v1.schemas.restaurants import (
    CreateRestaurantRequest,
    CreateRestaurantResponse,
    GetAllRestrauntsRequest,
    GetAllRestrauntsResponse,
    UpdateRestaurantRequest,
    UpdateRestaurantResponse
)
from app.application.commands.create_restaurant import CreateRestaurantCommand, CreateRestaurantHandler
from app.application.commands.update_restaurant import UpdateRestaurantCommand, UpdateRestaurantHandler
from app.application.queries.get_restraunts import GetAllRestrauntsQuery, GetAllRestrauntsHandler
from app.core.dependencies import get_creating_restaurant_handler, get_getting_all_restaurants_handler, get_updating_restaurant_handler

router = APIRouter(prefix="/restaurant", tags=["restaurants"])

@router.post("/", response_model=CreateRestaurantResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurant(request: CreateRestaurantRequest,
                            handler: CreateRestaurantHandler = Depends(get_creating_restaurant_handler)):
    
    command = CreateRestaurantCommand(name = request.name,
                                      address = request.address,
                                      contact_phone = request.contact_phone,
                                      opening_hours = request.opening_hours,
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

@router.patch("/", response_model=UpdateRestaurantResponse, status_code=status.HTTP_200_OK)
async def update_restaurant(
    request: UpdateRestaurantRequest,
    handler: UpdateRestaurantHandler = Depends(get_updating_restaurant_handler)
) -> UpdateRestaurantResponse:
    
    command = UpdateRestaurantCommand(
        id = request.id,
        name = request.name,
        address = request.address,
        contact_phone = request.contact_phone,
        opening_hours = request.opening_hours,
        is_active = request.is_active,
        description = request.description,
        coordinates = request.coordinates,
        tags = request.tags
    )

    result = await handler.handle(command)

    if result is None: 
        raise

    return UpdateRestaurantResponse(**result)