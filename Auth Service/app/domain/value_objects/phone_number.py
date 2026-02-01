from pydantic import BaseModel, field_validator
import re

class PhoneNumber(BaseModel):
    """Value Object to validate phone number"""
    value: str

    @field_validator('value')
    @classmethod
    def validate_phone_number(cls, value):
        v = re.sub(r'[\s\-\(\)]', '', v)
        pattern = r'^\+375(29|25|44|33|24)\d{7}$'

        if not re.match(pattern, value):
            raise ValueError("Invalid phone number format")
        
        return value