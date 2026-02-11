"""
    Create Restaurant Command and Handler
"""

from dataclasses import dataclass
from uuid import uuid4
from app.domain.entities.menu_category import MenuCategory
from app.domain.repositories.menu_category_repository import MenuCategoryRepository

@dataclass
class CreateMenuCategoryCommand:
    name: str

class CreateMenuCategoryHandler:

    def __init__(
        self,
        repo: MenuCategoryRepository
    ):
        self.repo = repo

    async def handle(self, command: CreateMenuCategoryCommand) -> dict:

        menu_category = MenuCategory(
            id=uuid4(),
            name=command.name
        )

        saved_menu_category = await self.repo.create(menu_category)

        return {
            "id": saved_menu_category.id,
            "msg": "Menu category successfully created!"
        }