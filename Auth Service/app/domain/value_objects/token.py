from pydantic import BaseModel, field_validator
from typing import ClassVar
from datetime import datetime

class AccessToken(BaseModel):
    """Value Object for access token"""
    value: str
    user_id: int
    expires_at: datetime

    MIN_TOKEN_LENGTH: ClassVar[int] = 20

    @field_validator('value')
    @classmethod
    def validate_token_value(cls, value: str) -> str:
        """Token format validation"""
        if not value or not value.strip():
            raise ValueError("Token value cannot be empty")
        if len(value) < cls.MIN_TOKEN_LENGTH:
            raise ValueError(f"Token must be at least {cls.MIN_TOKEN_LENGTH} characters")
        return value.strip()
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, value: int) -> int:
        """User id validation"""
        if value <= 0:
            raise ValueError("User id must be positive")
        return value
    
    def is_expired(self) -> bool:
        """Cheking token expiration"""
        return datetime.utcnow() >= self.expires_at
    
    def __str__(self) -> str:
        """Returning string representation of token"""
        return self.value
    
class RefreshToken(BaseModel):
    """Value Object for refressh token"""
    value: str
    user_id: int
    expires_at: datetime
    
    MIN_TOKEN_LENGTH: ClassVar[int] = 20
    
    @field_validator('value')
    @classmethod
    def validate_token_value(cls, value: str) -> str:
        """Token format validation"""
        if not value or not value.strip():
            raise ValueError("Token value cannot be empty")
        if len(value) < cls.MIN_TOKEN_LENGTH:
            raise ValueError(f"Token must be at least {cls.MIN_TOKEN_LENGTH} characters")
        return value.strip()
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, value: int) -> int:
        """User id validation"""
        if value <= 0:
            raise ValueError("User ID must be a positive integer")
        return value
    
    def is_expired(self) -> bool:
        """Cheking token expiration"""
        return datetime.utcnow() >= self.expires_at
    
    def __str__(self) -> str:
        """Returning string representation of token"""
        return self.value 