"""
Restaurant endpoint
"""

from fastapi import APIRouter, status, Depends, Query
from app.api.v1.schemas.restaurants import (
    CreateRestaurantRequest,
    CreateRestaurantResponse,
    GetAllRestrauntsRequest,
    GetAllRestrauntsResponse
)
from app.application.commands.create_restaurant import CreateRestaurantCommand, CreateRestaurantHandler
from app.application.queries.get_all_restraunts import GetAllRestrauntsQuery, GetAllRestrauntsHandler
from app.core.dependencies import get_creating_restaurant_handler, get_getting_all_restaurants_handler

router = APIRouter(prefix="/restaurant", tags=["restaurants"])

@router.post("/create", response_model=CreateRestaurantResponse, status_code=status.HTTP_201_CREATED)
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

@router.get("/get", response_model=GetAllRestrauntsResponse, status_code=status.HTTP_200_OK)
async def get_user_profile(
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