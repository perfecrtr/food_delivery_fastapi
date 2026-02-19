from uuid import UUID
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.repositories.payment_repository import PaymentRepository
from app.domain.entities.payment import Payment
from app.domain.enums import PaymentStatus
from app.infrastructure.db.mappers.payment_mapper import payment_entity_to_model, payment_model_to_entity
from app.infrastructure.db.models.payment import PaymentModel

class SQLAlchemyPaymentRepository(PaymentRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payment_data: Payment) -> Payment:
        payment_model = payment_entity_to_model(entity=payment_data)
        self.db.add(payment_model)
        await self.db.commit()
        await self.db.refresh(payment_model)
        return payment_model_to_entity(payment_model)

    async def get_by_id(self, payment_id: UUID) -> Optional[Payment]:
        stmt = select(PaymentModel).where(PaymentModel.id == payment_id)
        result = await self.db.execute(stmt)
        payment_model = result.scalar_one_or_none()

        return payment_model_to_entity(payment_model) if payment_model else None


    async def get_by_order_id(self, order_id: UUID) -> Optional[Payment]:
        stmt = select(PaymentModel).where(PaymentModel.order_id == order_id)
        result = await self.db.execute(stmt)
        payment_model = result.scalar_one_or_none()

        return payment_model_to_entity(payment_model) if payment_model else None


    async def update_status(self, payment_id: UUID, status: PaymentStatus) -> Optional[Payment]:
        stmt = select(PaymentModel).where(PaymentModel.id == payment_id)
        result = await self.db.execute(stmt)
        payment_model = result.scalar_one_or_none()

        if not payment_model:
            raise ValueError(f"Payment {payment_id} not found")
        
        payment_model.status = status
        payment_model.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(payment_model)

        return payment_model_to_entity(payment_model)