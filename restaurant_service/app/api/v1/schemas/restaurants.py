"""
    API Schemas for restaurants operations restaurant service endpoints
"""

from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.api.v1.schemas.dishes import DishInfo

class RestaurantInfo(BaseModel):
    id: UUID
    name: str
    address: str
    contact_phone: str
    opening_hours: dict
    is_active: Optional[bool] = None
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None

class CreateRestaurantRequest(BaseModel):   
    name: str
    address: str
    contact_phone: str
    opening_hours: dict
    is_active: Optional[bool] = None
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None

class CreateRestaurantResponse(BaseModel):
    """Response schema for restaurant creating"""

    id: UUID
    msg: str

class GetAllRestrauntsRequest(BaseModel):
    page: int = 0
    per_page: int = 10

class GetAllRestrauntsResponse(BaseModel):
    restraunts: list[RestaurantInfo]

class UpdateRestaurantRequest(RestaurantInfo):
    ...

class UpdateRestaurantResponse(RestaurantInfo):
    msg: str

class GetRestaurantMenuRequest(BaseModel):
    restaurant_id: UUID

class GetRestaurantMenuResponse(BaseModel):
    menu: list[DishInfo]
