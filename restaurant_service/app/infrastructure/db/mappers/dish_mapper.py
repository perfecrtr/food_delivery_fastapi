from app.domain.entities.dish import Dish
from app.infrastructure.db.models import DishModel

def dish_entity_to_model(entity: Dish) -> DishModel:
    return DishModel(
        id=entity.id,
        restaurant_id=entity.restaurant_id,
        price=entity.price,
        name=entity.name,
        category_id=entity.category_id,
        description=entity.description,
        weight=entity.weight,
        is_available=entity.is_available
    )


def dish_model_to_entity(model: DishModel) -> Dish:
    return Dish(
        id=model.id,
        restaurant_id=model.restaurant_id,
        price=model.price,
        name=model.name,
        category_id=model.category_id,
        description=model.description,
        weight=model.weight,
        is_available=model.is_available
    )