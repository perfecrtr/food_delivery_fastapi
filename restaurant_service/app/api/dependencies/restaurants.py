from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.database import get_db
from app.domain.repositories.restaurant_repository import RestaurantRepository
from app.infrastructure.db.repositories.restaurant_repository import (
    SQLAlchemyRestaurantRepository,
)
from app.application.commands.create_restaurant import CreateRestaurantHandler
from app.application.commands.update_restaurant import UpdateRestaurantHandler
from app.application.queries.get_restraunts import GetAllRestrauntsHandler
from app.application.queries.get_restraunt import GetRestaurantHandler
from app.application.queries.get_restraunt_menu import GetRestaurantMenuHandler
from app.domain.repositories.menu_repository import MenuRepository
from app.infrastructure.db.repositories.menu_repository import SQLAlchemyMenuRepository


async def get_restaurant_repository(
    db: AsyncSession = Depends(get_db),
) -> RestaurantRepository:
    return SQLAlchemyRestaurantRepository(db)


async def get_menu_repository(
    db: AsyncSession = Depends(get_db),
) -> MenuRepository:
    return SQLAlchemyMenuRepository(db)


async def get_creating_restaurant_handler(
    repo: RestaurantRepository = Depends(get_restaurant_repository),
) -> CreateRestaurantHandler:
    return CreateRestaurantHandler(repo)


async def get_getting_all_restaurants_handler(
    repo: RestaurantRepository = Depends(get_restaurant_repository),
) -> GetAllRestrauntsHandler:
    return GetAllRestrauntsHandler(repo)


async def get_restaurant_getting_handler(
    repo: RestaurantRepository = Depends(get_restaurant_repository),
) -> GetRestaurantHandler:
    return GetRestaurantHandler(repo)


async def get_updating_restaurant_handler(
    repo: RestaurantRepository = Depends(get_restaurant_repository),
) -> UpdateRestaurantHandler:
    return UpdateRestaurantHandler(repo)


async def get_restaurant_menu_getting_handler(
    repo: MenuRepository = Depends(get_menu_repository),
) -> GetRestaurantMenuHandler:
    return GetRestaurantMenuHandler(repo)