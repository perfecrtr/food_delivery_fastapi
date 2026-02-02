from dataclasses import dataclass

from app.domain.services.token_service import TokenService
from app.infrastructure.db.repository import UserRepository
from app.domain.value_objects.password import Password
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.domain.entities.user import User

@dataclass
class UserLoginCommand:
    phone_number: str
    password: str

class UserLoginHandler:
    def __init__(self,
                 user_repository: UserRepository,
                 password_hasher: BcryptPasswordHasher,
                 token_provider : TokenService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_provider = token_provider

    async def handle(self, command: UserLoginCommand):
        phone_number = PhoneNumber(command.phone_number)

        user = await self.user_repository.get_by_phone_number(phone_number)
        if not user:
            raise ValueError("Authorization Error")

        if not self.password_hasher.verify(command.password, user.hashed_password):
            raise ValueError("Authorization Error")

        access_token = self.token_provider.generate_access_token(user.id)
        refresh_token = self.token_provider.generate_refresh_token(user.id)

        return {
            "access_token" : access_token,
            "refresh_token" : refresh_token,
            "user" : {
                "id" : str(user.id),
                "full_name": str(user.full_name)
            }
        }