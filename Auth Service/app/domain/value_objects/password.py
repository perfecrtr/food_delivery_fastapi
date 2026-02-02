from pydantic import BaseModel, field_validator
import re
from typing import Optional, List

class Password(BaseModel):
    """Value Object to validate password"""
    value: str

    MIN_LENGTH = 8
    MAX_LENGTH = 30
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGITS = True
    REQUIRE_SPECIAL = True

    @field_validator('value')
    @classmethod
    def validate_password(cls, value: str) -> str:
        errors: List[str] = []

        if len(value) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters")

        if len(value) > cls.MAX_LENGTH:
            errors.append(f"Password must not exceed {cls.MAX_LENGTH} characters")
        
        if ' ' in value:
            errors.append("Password must not contain spaces.")
        
        if cls.REQUIRE_UPPERCASE and not any(char.isupper() for char in value):
            errors.append("Password must contain at least one capital letter (A-Z)")
        
        if cls.REQUIRE_LOWERCASE and not any(char.islower() for char in value):
            errors.append("Password must contain at least one lowercase letter(a-z)")
        
        if cls.REQUIRE_DIGITS and not any(char.isdigit() for char in value):
            errors.append("Password must contain at least one digit (0-9)")
        
        if cls.REQUIRE_SPECIAL and not re.search(cls.ALLOWED_SPECIAL_CHARS, value):
            errors.append(f"Password must contain at least one special symbol: ! @ # $ % ^ & * ( ) , . ? \" : {{ }} | < >")
        
        if errors:
            error_message = "Invalid password:\n" + "\n".join(f"• {error}" for error in errors)
            raise ValueError(error_message)
        
        return value
    
    def __str__(self) -> str:
        return self.value