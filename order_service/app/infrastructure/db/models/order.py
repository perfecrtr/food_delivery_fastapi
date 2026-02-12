from __future__ import annotations
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import List
from sqlalchemy import Uuid, DECIMAL, String, JSON, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.database import Base

class OrderModel(Base):
    """Order model in database"""
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    restaurant_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    user_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    delivery_address: Mapped[dict] = mapped_column(JSON)
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(10,2), nullable=False)
    status: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    delivered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    cancelled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now())

    items: Mapped[List['OrderItemModel']] = relationship(back_populates="order", cascade="all, delete-orphan")