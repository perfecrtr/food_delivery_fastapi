from __future__ import annotations
from typing import List
from uuid import UUID
from sqlalchemy import Uuid, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.database import Base

class MenuCategoryModel(Base):
    """Menu category model in database"""
    __tablename__ = "menu_categories"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    dishes: Mapped[List["DishModel"]] = relationship(back_populates="category", cascade="all, delete-orphan")