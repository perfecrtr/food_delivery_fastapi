"""
Register User Command and Handler
"""

from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.value_objects.password import Password
from app.infrastructure.db.repository import UserRepository
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_service import JWTService
from app.infrastructure.messaging.producer import KafkaEventProducer

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
        token_service: JWTService,
        kafka_producer: Optional[KafkaEventProducer]
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service
        self.kafka_producer = kafka_producer
    
    async def handle(self, command: RegisterUserCommand) -> Tuple[User, dict]:
        
        phone_vo = PhoneNumber(value=command.phone_number)
        password_vo = Password(value=command.password)
        normalized_phone = str(phone_vo.value)
        
        if await self.user_repository.exists_by_phone_number(normalized_phone):
            raise ValueError(f"User with phone {normalized_phone} already exists")
        
        user = User.create(
            phone_number=normalized_phone,
            password = password_vo.value,
            password_hasher = self.password_hasher,
            full_name=command.full_name
        )

        user_dict = {
            'phone_number': str(user.phone_number),
            'hashed_password': user.hashed_password,
            'full_name': user.full_name
        }
        
        saved_user = await self.user_repository.create(**user_dict)

        if self.kafka_producer:
            try:
                await self.kafka_producer.publish_user_registered(
                    user_id=saved_user.id,
                    phone_number=saved_user.phone_number,
                    fullname=saved_user.full_name
                )
            except Exception as e:
                ...
        
        access_token = self.token_service.generate_access_token(
            user_id=saved_user.id
        )
        refresh_token = self.token_service.generate_refresh_token(
            user_id=saved_user.id   
        )
                
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_at": datetime.utcnow() 
        }
        
        return saved_user, tokens
    