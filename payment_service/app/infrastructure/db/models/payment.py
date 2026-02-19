from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid, DECIMAL, Integer, Enum as SQLEnum, DateTime, func, String
from decimal import Decimal
from uuid import UUID
from datetime import datetime

from app.infrastructure.db.database import Base
from app.domain.enums import PaymentStatus, PaymentMethodType

class PaymentModel(Base):
    """Payment model in database"""
    __tablename__ = "payments"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    order_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer,nullable=False)
    restaurant_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10,2), nullable=False)
    transaction_id: Mapped[str] = mapped_column(String(20), nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus, native_enum=True), nullable=False)
    payment_method: Mapped[PaymentMethodType] = mapped_column(SQLEnum(PaymentMethodType, native_enum=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)