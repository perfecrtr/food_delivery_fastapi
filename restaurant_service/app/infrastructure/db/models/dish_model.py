from __future__ import annotations
from typing import Optional
from uuid import UUID
from sqlalchemy import Uuid, String, ForeignKey, Text, DECIMAL, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.infrastructure.db.database import Base

class DishModel(Base):
    """Dish model in database"""
    __tablename__ = "dishes"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    restaurant_id: Mapped[UUID] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    category_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("menu_categories.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    weight: Mapped[Optional[int]] = mapped_column(Integer)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    restaurant: Mapped["RestaurantModel"] = relationship(back_populates="dishes")
    category: Mapped["MenuCategoryModel"] = relationship(back_populates="dishes")