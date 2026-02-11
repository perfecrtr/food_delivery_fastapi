from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.entities.menu_category import MenuCategory
from app.domain.repositories.menu_category_repository import MenuCategoryRepository
from app.infrastructure.db.models import MenuCategoryModel
from app.infrastructure.db.mappers.menu_category_mapper import menu_category_entity_to_model, menu_category_model_to_entity

class SQLAlchemyMenuCategoryRepository(MenuCategoryRepository):

    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, menu_category_data: MenuCategory) -> MenuCategory:
        model = menu_category_entity_to_model(menu_category_data)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return menu_category_model_to_entity(model)

    async def get_menu_categories(self, offset: int, limit: int) -> List[MenuCategory]:
        stmt = select(MenuCategoryModel).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        
        categories = [menu_category_model_to_entity(model) for model in models]

        return categories if categories else []


