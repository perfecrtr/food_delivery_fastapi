from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from  uuid import UUID
from typing import Optional, List

from app.domain.repositories.courier_repository import CourierRepository
from app.domain.entities.courier import Courier
from app.domain.enums import CourierStatusEnum
from app.infrastructure.db.mappers.courier_mapper import courier_entity_to_model, courier_model_to_entity
from app.infrastructure.db.models import CourierModel

class SQLAlchemyCourierRepository(CourierRepository):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def get_by_id(self, courier_id: UUID) -> Optional[Courier]:
        stmt = select(CourierModel).where(CourierModel.id == courier_id)
        result = await self.db.execute(stmt)
        courier_model = result.scalar_one_or_none()

        return courier_model_to_entity(courier_model) if courier_model else None
    
    async def get_by_auth_id(self, auth_id: int) -> Optional[Courier]:
        stmt = select(CourierModel).where(CourierModel.auth_id == auth_id)
        result = await self.db.execute(stmt)
        courier_model = result.scalar_one_or_none()

        return courier_model_to_entity(courier_model) if courier_model else None
    
    async def create(self, courier: Courier) -> Courier:
       existing = await self.get_by_auth_id(courier.auth_id)
       if existing:
           raise ValueError(f"Courier with {courier.auth_id} auth_id already existing!")
       courier_model = courier_entity_to_model(courier)
       self.db.add(courier_model)
       await self.db.commit()
       await self.db.refresh(courier_model)
       return courier_model_to_entity(courier_model)
    
    async def update(self, courier: Courier) -> Courier:
        stmt = select(CourierModel).where(CourierModel.id == courier.id)
        result = await self.db.execute(stmt)
        courier_model = result.scalar_one_or_none()

        if not courier_model:
            raise ValueError(f"Courier {courier.id} not found")
        
        courier_model.status = courier.status.value
        courier_model.is_active = courier.is_active
        courier_model.updated_at = courier.updated_at

        await self.db.commit()
        await self.db.refresh(courier_model)  

        return courier_model_to_entity(courier_model)
    
    async def find_available(self, limit: int = 10) -> List[Courier]:
       stmt = select(CourierModel).where(
           CourierModel.is_active == True,
           CourierModel.status == CourierStatusEnum.AVAILABLE
       ).limit(limit)

       result = await self.db.execute(stmt)
       courier_models = result.scalars().all()

       return [courier_model_to_entity(courier_model) for courier_model in courier_models]