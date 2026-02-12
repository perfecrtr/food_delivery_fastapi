from uuid import UUID
from app.domain.value_objects import Address, OrderStatus, Money
from app.domain.entities.order import Order
from app.domain.enums import OrderStatusEnum
from app.infrastructure.db.models import OrderModel

def order_entity_to_model(entity: Order, order_id: UUID) -> OrderModel:
    return OrderModel(
        id=entity.id,
        restaurant_id=entity.id,
        user_id=entity.id,
        delivery_address={
            "city": entity.delivery_address.city,
            "street": entity.delivery_address.street,
            "house_number": entity.delivery_address.house_number,
            "apartment": entity.delivery_address.apartment,
            "entrance": entity.delivery_address.entrance,
            "floor": entity.delivery_address.floor
        },
        total_price=entity.total_price,
        status=entity.status.value,
        created_at=entity.created_at,
        delivered_at=entity.delivered_at,
        cancelled_at=entity.cancelled_at,
        updated_at=entity.updated_at
    )

def order_item_model_to_entity(model: OrderModel) -> Order:

    address = Address(
        city=model.delivery_address.get("city", ""),
        street=model.delivery_address.get("street", ""),
        house_number=model.delivery_address.get("house_number", ""),
        apartment=model.delivery_address.get("apartment", ""),
        entrance=model.delivery_address.get("entrance", ""),
        floor=model.delivery_address.get("floor", "")
    )

    status = OrderStatus(value=OrderStatusEnum(model.status), changed_at=model.updated_at)

    price = Money(model.total_price)

    return Order(
        id=model.id,
        restaurant_id=model.restaurant_id,
        user_id=model.user_id,
        address=address,
        total_price=price,
        status=status,
        created_at=model.created_at,
        delivered_at=model.delivered_at,
        cancelled_at=model.cancelled_at,
        updated_at=model.updated_at
    )