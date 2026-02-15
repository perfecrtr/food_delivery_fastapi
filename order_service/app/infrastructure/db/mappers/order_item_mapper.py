from uuid import UUID
from app.domain.entities.order_item import OrderItem
from app.domain.value_objects import Money
from app.infrastructure.db.models import OrderItemModel

def order_item_entity_to_model(entity: OrderItem, order_id: UUID) -> OrderItemModel:
    return OrderItemModel(
        id=entity.id,
        order_id=order_id,
        dish_id=entity.dish_id,
        name = entity.name,
        price = entity.price.amount,
        quantity = entity.quantity
    )

def order_item_model_to_entity(model: OrderItemModel) -> OrderItem:
    return OrderItem(
        id=model.id,
        dish_id=model.dish_id,
        name=model.name,
        price=Money(amount=model.price),
        quantity=model.quantity
    )