"""
Register User Command and Handler
"""

from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from domain.entities.user import User
from domain.value_objects.phone_number import PhoneNumber
from domain.value_objects.password import Password
from infrastructure.db.repository import UserRepository
from infrastructure.security.password_hasher import BcryptPasswordHasher
from infrastructure.security.jwt_service import JWTService
from domain.events import UserRegistered, UserLoggedIn


@dataclass
class RegisterUserCommand:
    phone_number: str
    password: str
    full_name: Optional[str] = None

class RegisterUserHandler:
    """
    Command Handler for User Registration 
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: BcryptPasswordHasher,
        token_service: JWTService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service
    
    async def execute(self, command: RegisterUserCommand) -> Tuple[User, dict]:
        
        phone_vo = PhoneNumber(value=command.phone_number)
        password_vo = Password(value=command.password)
        normalized_phone = str(phone_vo.value)
        
        if self.user_repository.exists_by_phone_number(normalized_phone):
            raise ValueError(f"User with phone {normalized_phone} already exists")
        
        user = User.create(
            phone_number=normalized_phone,
            password = password_vo,
            password_hasher = self.password_hasher,
            full_name=command.full_name
        )
        
        saved_user = self.user_repository.create(user)
        
        access_token = self.token_service.generate_access_token(
            data={"sub": saved_user.id}
        )
        refresh_token = self.token_service.generate_refresh_token(
            data={"sub": saved_user.id}
        )
                
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_at": datetime.utcnow() 
        }
        
        return saved_user, tokens
    