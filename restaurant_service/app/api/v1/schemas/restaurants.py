"""
    API Schemas for restaurants operations restaurant service endpoints
"""

from pydantic import BaseModel, Field, UUID4, ConfigDict
from uuid import UUID
from typing import Optional, List
from enum import Enum
from app.api.v1.schemas.dishes import DishInfo

class AddressSchema(BaseModel):
    city: str = Field(..., description="Город", example="Минск")
    street: str = Field(..., description="Улица", example="Крутая")
    house_number: str = Field(..., description="Номер дома", example="8")
    building: Optional[str] = Field(None, description="Корпус", example="1")
    floor: Optional[str] = Field(None, description="Этаж", example="цокольный")

class RestaurantInfo(BaseModel):
    id: UUID
    name: str
    address: str
    contact_phone: str
    schedule: dict
    is_active: Optional[bool] = None
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None

class CreateRestaurantRequest(BaseModel):   
    name: str
    address: AddressSchema
    contact_phone: str
    schedule: dict
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

class GetRestaurantRequest(BaseModel):
    id: UUID

class GetRestaurantResponse(RestaurantInfo):
    ...

class UpdateRestaurantRequest(BaseModel):
    id: UUID
    name: str
    address: AddressSchema
    contact_phone: str
    schedule: dict
    is_active: Optional[bool] = None
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None

class UpdateRestaurantResponse(BaseModel):
    id: UUID
    name: str
    address: str
    contact_phone: str
    schedule: dict
    is_active: Optional[bool] = None
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None
    msg: str

class GetRestaurantMenuRequest(BaseModel):
    restaurant_id: UUID

class GetRestaurantMenuResponse(BaseModel):
    menu: list[DishInfo]

class ValidationItemRequest(BaseModel):
    dish_id: UUID4
    quantity: int

class ValidateOrderRequest(BaseModel):
    items: List[ValidationItemRequest]
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "dish_id": "123e4567-e89b-12d3-a456-426614174000",
                        "quantity": 2
                    },
                    {
                        "dish_id": "987fcdeb-51a3-43b7-a456-426614174222",
                        "quantity": 1
                    }
                ]
            }
        }
    )

class ValidatedItemResponse(BaseModel):
    dish_id: UUID4
    name: str
    price: float
    quantity: int

class ValidateOrderResponse(BaseModel):
    is_valid: bool
    validated_items: List[ValidatedItemResponse]
    errors: List

