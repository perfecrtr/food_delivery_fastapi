from app.domain.entities.courier import Courier
from app.infrastructure.db.models import CourierModel
from app.domain.value_objects import CourierStatus
from app.domain.enums import CourierStatusEnum

def courier_entity_to_model(entity: Courier) -> CourierModel:
    return CourierModel(
        id=entity.id,
        auth_id=entity.auth_id,
        name=entity.name,
        phone=entity.phone,
        is_active=entity.is_active,
        status=entity.status.value,
        created_at=entity.created_at,
        updated_at=entity.updated_at
    )

def courier_model_to_entity(model: CourierModel) -> Courier:

    status = CourierStatus(value=CourierStatusEnum(model.status))

    return Courier(
        id=model.id,
        auth_id=model.auth_id,
        name=model.name,
        phone=model.phone,
        is_active=model.is_active,
        status=status,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )