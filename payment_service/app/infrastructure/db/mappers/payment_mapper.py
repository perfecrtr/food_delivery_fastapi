from app.domain.entities.payment import Payment
from app.domain.value_objects.money import Money
from app.infrastructure.db.models.payment import PaymentModel

def payment_entity_to_model(entity: Payment) -> PaymentModel:
    return PaymentModel(
        id=entity.id,
        order_id=entity.order_id,
        user_id=entity.user_id,
        restaurant_id=entity.restaurant_id,
        amount=entity.amount.amount,
        status=entity.status,
        payment_method=entity.payment_method,
        created_at=entity.created_at,
        updated_at=entity.updated_at
    )

def payment_model_to_entity(model: PaymentModel) -> Payment:
    return Payment(
        id=model.id,
        order_id=model.order_id,
        user_id=model.user_id,
        restaurant_id=model.restaurant_id,
        amount=Money(amount=model.amount),
        status=model.status,
        payment_method=model.payment_method,
        created_at=model.created_at,
        updated_at=model.updated_at
    )