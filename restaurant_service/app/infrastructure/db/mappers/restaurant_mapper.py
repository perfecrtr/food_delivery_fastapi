from app.domain.entities.restaurant import Restaurant
from app.infrastructure.db.models import RestaurantModel
from app.domain.value_objects import PhoneNumber, Address

def restaurant_entity_to_model(entity: Restaurant) -> RestaurantModel:
    return RestaurantModel(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        address=entity.address.full_address,
        coordinates=entity.coordinates,
        contact_phone=str(entity.contact_phone),
        is_active=entity.is_active,
        schedule=entity.schedule,
        tags=entity.tags,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def restaurant_model_to_entity(model: RestaurantModel) -> Restaurant:
    return Restaurant(
        id=model.id,
        name=model.name,
        address=Address.from_model(model.address),
        contact_phone=PhoneNumber(model.contact_phone),
        is_active=model.is_active,
        schedule=model.schedule,
        created_at=model.created_at,
        description=model.description,
        coordinates=model.coordinates,
        tags=model.tags,
        updated_at=model.updated_at,
    )