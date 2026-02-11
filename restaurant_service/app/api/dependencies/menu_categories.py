from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.database import get_db
from app.domain.repositories.menu_category_repository import MenuCategoryRepository
from app.infrastructure.db.repositories.menu_category_repository import (
    SQLAlchemyMenuCategoryRepository,
)
from app.application.commands.create_menu_category import CreateMenuCategoryHandler
from app.application.queries.get_menu_categories import GetMenuCategoriesHandler


async def get_menu_category_repository(
    db: AsyncSession = Depends(get_db),
) -> MenuCategoryRepository:
    return SQLAlchemyMenuCategoryRepository(db)


async def get_menu_category_creating_handler(
    repo: MenuCategoryRepository = Depends(get_menu_category_repository),
) -> CreateMenuCategoryHandler:
    return CreateMenuCategoryHandler(repo)


async def get_menu_categories_getting_handler(
    repo: MenuCategoryRepository = Depends(get_menu_category_repository),
) -> GetMenuCategoriesHandler:
    return GetMenuCategoriesHandler(repo)