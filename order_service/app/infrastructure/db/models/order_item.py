from __future__ import annotations
from uuid import UUID
from decimal import Decimal
from sqlalchemy import Uuid, DECIMAL, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.database import Base

class OrderItemModel(Base):
    """Order item model in database"""
    __tablename__ = "order_items"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    dish_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(5,2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped["OrderModel"] = relationship(back_populates="items")