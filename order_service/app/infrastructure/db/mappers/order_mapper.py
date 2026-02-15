from uuid import UUID
from typing import List
from app.domain.value_objects import Address, OrderStatus, Money
from app.domain.entities.order import Order
from app.domain.entities.order_item import OrderItem
from app.domain.enums import OrderStatusEnum
from app.infrastructure.db.models import OrderModel
from app.infrastructure.db.mappers.order_item_mapper import order_item_model_to_entity

def order_entity_to_model(entity: Order) -> OrderModel:
    return OrderModel(
        id=entity.id,
        restaurant_id=entity.restaurant_id,
        user_id=entity.user_id,
        delivery_address={
            "city": entity.delivery_address.city,
            "street": entity.delivery_address.street,
            "house_number": entity.delivery_address.house_number,
            "apartment": entity.delivery_address.apartment,
            "entrance": entity.delivery_address.entrance,
            "floor": entity.delivery_address.floor
        },
        total_price=entity.total_price.amount,
        status=entity.status.value,
        created_at=entity.created_at,
        delivered_at=entity.delivered_at,
        cancelled_at=entity.cancelled_at,
        updated_at=entity.updated_at
    )

def order_model_to_entity(model: OrderModel, include_items: bool = True) -> Order:

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

    items: List[OrderItem] = []
    if include_items and hasattr(model, 'items'):
        items = [
            order_item_model_to_entity(item) 
            for item in model.items
        ]

    return Order(
        id=model.id,
        restaurant_id=model.restaurant_id,
        user_id=model.user_id,
        items=items,
        delivery_address=address,
        total_price=price,
        status=status,
        created_at=model.created_at,
        delivered_at=model.delivered_at,
        cancelled_at=model.cancelled_at,
        updated_at=model.updated_at
    )