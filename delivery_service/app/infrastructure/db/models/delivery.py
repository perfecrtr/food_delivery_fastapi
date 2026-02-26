from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, String, Enum as SQLEnum, DateTime, func, ForeignKey, JSON
from uuid import UUID 
from datetime import datetime
from typing import Optional

from app.infrastructure.db.database import Base
from app.domain.enums import DeliveryStatusEnum

class DeliveryModel(Base):
    __tablename__ = "deliveries"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    order_id: Mapped[UUID] = mapped_column(Uuid, unique=True, index=True, nullable=False)
    courier_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey('couriers.id'), nullable=True,  index=True)
    restaurant_address: Mapped[dict] = mapped_column(JSON, nullable=False)
    delivery_address: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[DeliveryStatusEnum] = mapped_column(SQLEnum(DeliveryStatusEnum, native_enum=True), nullable=False, default=DeliveryStatusEnum.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    assigned_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    picked_up_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    cancelled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    failed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    courier: Mapped["CourierModel"] = relationship(back_populates="deliveries")
    