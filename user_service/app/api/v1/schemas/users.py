"""
    API schemas for user service endpoints
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.domain.enums import Gender

class CreateUserProfileRequest(BaseModel):
    """Request schema for user profile creating"""
    id: int
    phone_number: str
    full_name: str

class CreateUserProfileResponse(BaseModel):
    id: int
    msg: str

class GetUserProfileRequest(BaseModel):
    id: int

class GetUserProfileResponse(BaseModel):
    id: int
    phone_number: str
    full_name: str
    email: Optional[str]
    address: Optional[str]
    birthday_date: Optional[date]
    gender: Optional[Gender]



