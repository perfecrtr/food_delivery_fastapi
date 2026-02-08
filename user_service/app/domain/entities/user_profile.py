from dataclasses import dataclass
from sqlalchemy import Date
from datetime import datetime
from app.domain.enums import Gender
from typing import Optional

@dataclass
class UserProfile():
    """
    Domain entity representation for User Profile
    """
    id: int 
    phone_number: str
    fullname: str
    email: Optional[str]
    address: Optional[str]
    birthday_date: Optional[Date]
    gender: Optional[Gender]
    created_at: datetime
    updated_at: Optional[datetime]