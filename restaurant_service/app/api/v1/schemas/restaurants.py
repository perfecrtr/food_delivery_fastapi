"""
    API Schemas for restaurants operations restaurant service endpoints
"""

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CreateRestaurantRequest(BaseModel):
    
    name: str
    address: str
    contact_phone: str
    is_active: bool
    opening_hourst: dict
    description: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[list] = None

class CreateRestaurantResponse(BaseModel):
    """Response schema for restaurant creating"""

    id: UUID
    msg: str