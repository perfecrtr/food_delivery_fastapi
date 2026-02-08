"""
    Create User Profile Command and Handler
"""

from dataclasses import dataclass
from app.domain.entities.user_profile import UserProfile
from app.infrastructure.db.repository import UserProfileRepository

@dataclass
class CreateUserProfileCommand:
    id: int
    phone_number: str
    fullname: str

class CreateUserProfileHandler:

    def __init__(
        self,
        user_profile_repository: UserProfileRepository
    ):
        self.user_profile_repository = user_profile_repository

    async def handle(self, command: CreateUserProfileCommand) -> dict:
        
        if await self.user_profile_repository.exists(command.id) or await self.user_profile_repository.exists_by_phone_number(command.phone_number):
            raise ValueError(f"User exists")
    
        user_profile = UserProfile(
            id = command.id,
            phone_number = command.phone_number,
            fullname = command.fullname
        )

        saved_user_profile = await self.user_profile_repository.create_user_profile(user_profile)

        return {
            "id": saved_user_profile.id,
            "phone_number": saved_user_profile.phone_number,
            "fullname": saved_user_profile.fullname,
            "email": saved_user_profile.email,
            "address": saved_user_profile.address,
            "birthday_date": saved_user_profile.birthday_date,
            "gender": saved_user_profile.gender 
        }

        

        


