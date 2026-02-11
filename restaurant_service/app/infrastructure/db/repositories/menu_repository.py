from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.entities.dish import Dish
from app.domain.repositories.menu_repository import MenuRepository
from app.infrastructure.db.models import DishModel, MenuCategoryModel

class SQLAlchemyMenuRepository(MenuRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_restaurant_menu(self, restaurant_id: UUID) -> List[Dish]:
        stmt = select(
            DishModel.id,
            MenuCategoryModel.name.label("category_name"),
            DishModel.name,
            DishModel.price,
            DishModel.description,
            DishModel.weight,
            DishModel.is_available
        ).join(
            MenuCategoryModel,
            DishModel.category_id==MenuCategoryModel.id,
            isouter=True
        ).where(
            DishModel.restaurant_id == restaurant_id
        )
        result = await self.db.execute(stmt)
        return [dict(row._mapping) for row in result.all()]

