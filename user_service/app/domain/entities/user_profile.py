from dataclasses import dataclass, field
from datetime import date
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
    email: Optional[str] = None
    address: Optional[str] = None
    birthday_date: Optional[date] = None
    gender: Optional[Gender] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None