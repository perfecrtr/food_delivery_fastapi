from dataclasses import dataclass
from typing import Optional

from app.domain.repositories.menu_category_repository import MenuCategoryRepository

@dataclass
class GetMenuCategoriesQuery:
    page: int = 0
    per_page: int = 10

class GetMenuCategoriesHandler:

    def __init__(
        self,
        repo: MenuCategoryRepository
    ):
        self.repo = repo

    async def handle(self, query: GetMenuCategoriesQuery) -> Optional[dict]:
        
        offset = query.page * query.per_page

        menu_categories = await self.repo.get_menu_categories(
            offset=offset, 
            limit=query.per_page)

        if not menu_categories:
            raise

        return [{
            "id": menu_category.id,
            "name": menu_category.name,
        }
        for menu_category in menu_categories]