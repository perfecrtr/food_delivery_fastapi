from app.domain.entities.restaurant import Restaurant
from app.infrastructure.db.models import RestaurantModel

def restaurant_entity_to_model(entity: Restaurant) -> RestaurantModel:
    return RestaurantModel(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        address=entity.address,
        coordinates=entity.coordinates,
        contact_phone=entity.contact_phone,
        is_active=entity.is_active,
        opening_hours=entity.opening_hours,
        tags=entity.tags,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def restaurant_model_to_entity(model: RestaurantModel) -> Restaurant:
    return Restaurant(
        id=model.id,
        name=model.name,
        address=model.address,
        contact_phone=model.contact_phone,
        is_active=model.is_active,
        opening_hours=model.opening_hours,
        created_at=model.created_at,
        description=model.description,
        coordinates=model.coordinates,
        tags=model.tags,
        updated_at=model.updated_at,
    )