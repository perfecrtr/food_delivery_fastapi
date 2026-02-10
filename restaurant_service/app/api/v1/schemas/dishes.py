"""
    API Schemas for dishes operations restaurant service endpoints
"""

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CreateDishRequest(BaseModel):   
    restaurant_id: UUID
    price: float
    name: str
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    weight: Optional[int] = None
    is_available: Optional[bool] = None

class CreateDishResponse(BaseModel):

    id: UUID
    msg: str

class UpdateDishRequest(BaseModel):
    id: UUID
    restaurant_id: UUID
    price: float
    name: str
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    weight: Optional[int] = None
    is_available: Optional[bool] = None

class UpdateDishResponse(BaseModel):
    id: UUID
    restaurant_id: UUID
    price: float
    name: str
    msg: str
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    weight: Optional[int] = None
    is_available: Optional[bool] = None

