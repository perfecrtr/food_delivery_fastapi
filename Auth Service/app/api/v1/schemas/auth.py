"""
API schemas for authentication endpoints
"""

from pydantic import BaseModel, field_validator, Field
from typing import Optional
from datetime import datetime
import re


class RegisterRequest(BaseModel):
    """Request schema for user registration"""
    phone_number: str
    password: str
    full_name: Optional[str] = None
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        """Validate phone number format"""
        if not value:
            raise ValueError("Phone number cannot be empty")
        cleaned = re.sub(r'[\s\-\(\)]', '', value)
        pattern = r'^\+375(29|25|44|33|24)\d{7}$'
        if not re.match(pattern, cleaned):
            raise ValueError("Invalid phone number format. Expected format: +375XXXXXXXXX")
        return cleaned
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Basic password validation"""
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(value) > 30:
            raise ValueError("Password must not exceed 30 characters")
        if ' ' in value:
            raise ValueError("Password must not contain spaces")
        return value
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+375291234567",
                "password": "Password123!",
                "full_name": "John Doe"
            }
        }


class LoginRequest(BaseModel):
    """Request schema for user login"""
    phone_number: str
    password: str
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        """Validate phone number format"""
        if not value:
            raise ValueError("Phone number cannot be empty")
        cleaned = re.sub(r'[\s\-\(\)]', '', value)
        pattern = r'^\+375(29|25|44|33|24)\d{7}$'
        if not re.match(pattern, cleaned):
            raise ValueError("Invalid phone number format")
        return cleaned
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Basic password validation"""
        if not value:
            raise ValueError("Password cannot be empty")
        return value
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+375291234567",
                "password": "Password123!"
            }
        }

class ChangePasswordRequest(BaseModel):
    phone_number: str = Field(..., pattern=r'^(\+375)\d{9}$')
    old_password: str = Field(..., min_length=8, max_length=30)
    new_password: str = Field(..., min_length=8, max_length=30)


    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        """Validate phone number format"""
        if not value:
            raise ValueError("Phone number cannot be empty")
        cleaned = re.sub(r'[\s\-\(\)]', '', value)
        pattern = r'^\+375(29|25|44|33|24)\d{7}$'
        if not re.match(pattern, cleaned):
            raise ValueError("Invalid phone number format")
        return cleaned
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        """Validate new password"""
        if not value:
            raise ValueError("New password cannot be empty")
        if len(value) < 8:
            raise ValueError("New password must be at least 8 characters")
        if len(value) > 30:
            raise ValueError("New password must not exceed 30 characters")
        if ' ' in value:
            raise ValueError("New password must not contain spaces")
        return value
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+375291234567",
                "old_password": "OldPassword123!",
                "new_password": "NewPassword123!"
            }
        }

class TokenResponse(BaseModel):
    """Response schema for token pair"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class LoginResponse(TokenResponse):
    """Response schema for login endpoint"""
    pass

class RegisterResponse(BaseModel):
    """Response schema for registration"""
    user_id : int
    created_at: datetime

class RefreshTokenRequest(BaseModel):
    """Request schema for refreshing access token"""
    refresh_token: str
    
    @field_validator('refresh_token')
    @classmethod
    def validate_refresh_token(cls, value: str) -> str:
        """Validate refresh token"""
        if not value or not value.strip():
            raise ValueError("Refresh token cannot be empty")
        if len(value) < 20:
            raise ValueError("Invalid refresh token format")
        return value.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }

class ChangePasswordResponse(BaseModel):
    success: str
    message: str
    user_id: int

class RefreshTokenResponse(TokenResponse):
    """Response schema for refresh endpoint"""
    pass




