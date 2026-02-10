"""
    Create Restaurant Command and Handler
"""

from dataclasses import dataclass
from uuid import uuid4
from app.domain.entities.menu_category import MenuCategory
from app.infrastructure.db.repository import MenuCategoryRepository

@dataclass
class CreateMenuCategoryCommand:
    name: str

class CreateMenuCategoryHandler:

    def __init__(
        self,
        menu_category_repository: MenuCategoryRepository
    ):
        self.menu_category_repository = menu_category_repository

    async def handle(self, command: CreateMenuCategoryCommand) -> dict:

        menu_category = MenuCategory(
            id=uuid4(),
            name=command.name
        )

        saved_menu_category = await self.menu_category_repository.create_menu_category(menu_category)

        return {
            "id": saved_menu_category.id,
            "msg": "Menu category successfully created!"
        }