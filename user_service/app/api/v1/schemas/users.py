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
    fullname: str

class CreateUserProfileResponse(BaseModel):
    id: int
    phone_number: str
    fullname: str
    msg: str

class GetUserProfileResponse(BaseModel):
    id: int
    phone_number: str
    fullname: str
    email: Optional[str] = None
    address: Optional[str] = None
    birthday_date: Optional[date] = None
    gender: Optional[Gender] = None

class UpdateUserProfileRequest(BaseModel):
    id: int
    phone_number: str
    fullname: str
    email: Optional[str] = None
    address: Optional[str] = None
    birthday_date: Optional[date] = None
    gender: Optional[Gender] = None

class UpdateUserProfileRequest(BaseModel):
    id: int
    phone_number: str
    fullname: str
    email: Optional[str] = None
    address: Optional[str] = None
    birthday_date: Optional[date] = None
    gender: Optional[Gender] = None
    msg: str