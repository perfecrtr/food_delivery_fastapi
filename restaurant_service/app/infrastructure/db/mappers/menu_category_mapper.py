from app.domain.entities.menu_category import MenuCategory
from app.infrastructure.db.models import MenuCategoryModel

def menu_category_entity_to_model(entity: MenuCategory) -> MenuCategoryModel:
    return MenuCategoryModel(
        id=entity.id,
        name=entity.name
    )


def menu_category_model_to_entity(model: MenuCategoryModel) -> MenuCategory:
    return MenuCategory(
        id=model.id,
        name=model.name
    )