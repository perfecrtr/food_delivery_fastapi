"""
    Create User Profile Command and Handler
"""

from dataclasses import dataclass
from typing import Optional
from datetime import date
from app.domain.enums import Gender
from app.domain.entities.user_profile import UserProfile
from app.infrastructure.db.repository import UserProfileRepository

@dataclass
class UpdateUserProfileCommand:
    id: int
    fullname: str
    email: Optional[str] = None
    address: Optional[str] = None
    birthday_date: Optional[date] = None
    gender: Optional[Gender] = None

class UpdateUserProfileHandler:

    def __init__(
        self,
        user_profile_repository: UserProfileRepository
    ):
        self.user_profile_repository = user_profile_repository

    async def handle(self, command: UpdateUserProfileCommand) -> dict:
        
        if not await self.user_profile_repository.exists(command.id):
            raise ValueError(f"User doesn't exist")
    
        user_profile_update_data = {
            "fullname": command.fullname,
            "email": command.email,
            "address": command.address,
            "birthday_date": command.birthday_date,
            "gender": command.gender
        }

        updated_user_profile = await self.user_profile_repository.update(command.id, **user_profile_update_data)

        return {
            "id": updated_user_profile.id,
            "phone_number": updated_user_profile.phone_number,
            "fullname": updated_user_profile.fullname,
            "email": updated_user_profile.email,
            "address": updated_user_profile.address,
            "birthday_date": updated_user_profile.birthday_date,
            "gender": updated_user_profile.gender,
            "msg": "Profile updated successfully"
        }

        

        


