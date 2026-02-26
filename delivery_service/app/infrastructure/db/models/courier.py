from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, Integer, String, Boolean, Enum as SQLEnum, DateTime, func, ForeignKey
from uuid import UUID 
from datetime import datetime
from typing import Optional, List

from app.infrastructure.db.database import Base
from app.domain.enums import CourierStatusEnum

class CourierModel(Base):
    __tablename__ = "couriers"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    auth_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status: Mapped[CourierStatusEnum] = mapped_column(SQLEnum(CourierStatusEnum, native_enum=True), nullable=False, default=CourierStatusEnum.OFFLINE)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    deliveries: Mapped[List["DeliveryModel"]] = relationship(back_populates="courier")
    