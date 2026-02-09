from typing import Optional, List
from uuid import UUID
from sqlalchemy import Uuid, String, JSON, Boolean, DateTime, func, ForeignKey, Text, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.infrastructure.db.database import Base

class RestaurantModel(Base):
    """Restraunt model in database"""
    __tablename__ = "restaurants"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(100), nullable = False)
    coordinates: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    opening_hours: Mapped[dict] = mapped_column(JSON, nullable=False)
    tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    dishes: Mapped[List["DishModel"]] = relationship(back_populates="restaurant", cascade="all, delete-orphan")

class MenuCategoryModel(Base):
    """Menu category model in database"""
    __tablename__ = "menu_categories"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    dishes: Mapped[List["DishModel"]] = relationship(back_populates="category", cascade="all, delete-orphan")

class DishModel(Base):
    """Dish model in database"""
    __tablename__="dishes"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    restaurant_id: Mapped[UUID] = mapped_column(ForeignKey("restaurants.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("menu_categories.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(30), unique=False, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    weight: Mapped[Optional[int]] = mapped_column(Integer)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    restaurant: Mapped["RestaurantModel"] = relationship(back_populates="dishes")
    category: Mapped["MenuCategoryModel"] = relationship(back_populates="dishes")




