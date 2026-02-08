from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.application.commands.create_user_profile import CreateUserProfileHandler
from app.application.queries.get_user_profile import GetUserProfileHandler
from app.infrastructure.db.database import get_db
from app.infrastructure.db.repository import UserProfileRepository



async def get_user_profile_repository(db: AsyncSession = Depends(get_db)) -> UserProfileRepository:
    """
    Get user repository instance
    """
    return UserProfileRepository(db)

async def get_creating_profile_handler(user_profile_repository = Depends(get_user_profile_repository)):
    return(
        CreateUserProfileHandler(
        user_profile_repository
        )
    )

async def get_get_user_profile_handler(user_profile_repository = Depends(get_user_profile_repository)):
    return(
        GetUserProfileHandler(
            user_profile_repository
        )
    )