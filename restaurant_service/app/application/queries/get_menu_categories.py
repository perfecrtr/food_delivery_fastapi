from dataclasses import dataclass
from typing import Optional

from app.infrastructure.db.repository import MenuCategoryRepository

@dataclass
class GetMenuCategoriesQuery:
    page: int = 0
    per_page: int = 10

class GetMenuCategoriesHandler:

    def __init__(
        self,
        menu_category_repository: MenuCategoryRepository
    ):
        self.menu_category_repository = menu_category_repository

    async def handle(self, query: GetMenuCategoriesQuery) -> Optional[dict]:
        
        offset = query.page * query.per_page

        menu_categories = await self.menu_category_repository.get_all(
            skip=offset, 
            limit=query.per_page)

        if not menu_categories:
            raise

        return [{
            "id": menu_category.id,
            "name": menu_category.name,
        }
        for menu_category in menu_categories]