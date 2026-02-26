from app.domain.entities.delivery import Delivery
from app.infrastructure.db.models import DeliveryModel
from app.domain.value_objects import Address, DeliveryStatus
from app.domain.enums import DeliveryStatusEnum

def delivery_entity_to_model(entity: Delivery) -> DeliveryModel:
    return DeliveryModel(
        id=entity.id,
        order_id=entity.order_id,
        courier_id=entity.courier_id,
        restaurant_address={
            "city": entity.restaurant_address.city,
            "street": entity.restaurant_address.street,
            "house_number": entity.restaurant_address.house_number,
            "apartment": entity.restaurant_address.apartment,
            "entrance": entity.restaurant_address.entrance,
            "floor": entity.restaurant_address.floor
        },
        delivery_address={
            "city": entity.delivery_address.city,
            "street": entity.delivery_address.street,
            "house_number": entity.delivery_address.house_number,
            "apartment": entity.delivery_address.apartment,
            "entrance": entity.delivery_address.entrance,
            "floor": entity.delivery_address.floor
        },
        status=entity.status.value,
        created_at=entity.created_at,
        assigned_at=entity.assigned_at,
        picked_up_at=entity.picked_up_at,
        delivered_at=entity.delivered_at,
        cancelled_at=entity.cancelled_at,
        failed_at=entity.failed_at,
        updated_at=entity.updated_at
    )

def delivery_model_to_entity(model: DeliveryModel) -> Delivery:

    restaurant_address = Address(
        city=model.restaurant_address.get("city", ""),
        street=model.restaurant_address.get("street", ""),
        house_number=model.restaurant_address.get("house_number", ""),
        apartment=model.restaurant_address.get("apartment", ""),
        entrance=model.restaurant_address.get("entrance", ""),
        floor=model.restaurant_address.get("floor", "")
    )

    delivery_address = Address(
        city=model.delivery_address.get("city", ""),
        street=model.delivery_address.get("street", ""),
        house_number=model.delivery_address.get("house_number", ""),
        apartment=model.delivery_address.get("apartment", ""),
        entrance=model.delivery_address.get("entrance", ""),
        floor=model.delivery_address.get("floor", "")
    )

    status = DeliveryStatus(value=DeliveryStatusEnum(model.status))

    return Delivery(
        id=model.id,
        order_id=model.order_id,
        courier_id=model.courier_id,
        restaurant_address=restaurant_address,
        delivery_address=delivery_address,
        status=status,
        created_at=model.created_at,
        assigned_at=model.assigned_at,
        picked_up_at=model.picked_up_at,
        delivered_at=model.delivered_at,
        cancelled_at=model.cancelled_at,
        failed_at=model.failed_at,
        updated_at=model.updated_at,
    )