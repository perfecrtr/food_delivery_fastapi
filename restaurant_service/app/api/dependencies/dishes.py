from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.database import get_db
from app.domain.repositories.dish_repository import DishRepository
from app.infrastructure.db.repositories.dish_repository import SQLAlchemyDishRepository
from app.application.commands.create_dish import CreateDishHandler
from app.application.commands.update_dish import UpdateDishHandler


async def get_dish_repository(
    db: AsyncSession = Depends(get_db),
) -> DishRepository:
    return SQLAlchemyDishRepository(db)


async def get_dish_creating_handler(
    repo: DishRepository = Depends(get_dish_repository),
) -> CreateDishHandler:
    return CreateDishHandler(repo)


async def get_dish_updating_handler(
    repo: DishRepository = Depends(get_dish_repository),
) -> UpdateDishHandler:
    return UpdateDishHandler(repo)