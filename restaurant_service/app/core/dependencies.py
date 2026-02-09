from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.application.commands.create_restaurant import CreateRestaurantHandler
from app.application.queries.get_all_restraunts import GetAllRestrauntsHandler
from app.infrastructure.db.database import get_db
from app.infrastructure.db.repository import RestaurantRepository



async def get_user_profile_repository(db: AsyncSession = Depends(get_db)) -> RestaurantRepository:
    """
    Get user repository instance
    """
    return RestaurantRepository(db)

async def get_creating_restaurant_handler(user_profile_repository = Depends(get_user_profile_repository)):
    return(
        CreateRestaurantHandler(
        user_profile_repository
        )
    )

async def get_getting_all_restaurants_handler(user_profile_repository = Depends(get_user_profile_repository)):
    return(
        GetAllRestrauntsHandler(
        user_profile_repository
        )
    )