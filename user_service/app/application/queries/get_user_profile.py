from dataclasses import dataclass
from typing import Optional

from app.infrastructure.db.repository import UserProfileRepository

@dataclass
class GetUserProfileQuery:
    id: int

class GetUserProfileHandler:

    def __init__(
        self,
        user_profile_repository: UserProfileRepository
    ):
        self.user_profile_repository = user_profile_repository

    async def handle(self, query: GetUserProfileQuery) -> Optional[dict]:
        user_profile = await self.user_profile_repository.get_by_id(query.id)

        if not user_profile:
            return None
        
        return{
            "id": user_profile.id,
            "phone_number": user_profile.phone_number,
            "fullname": user_profile.fullname,
            "email": user_profile.email,
            "address": user_profile.address,
            "birthday_date": user_profile.birthday_date,
            "gender": user_profile.gender.value if user_profile.gender else None
        }