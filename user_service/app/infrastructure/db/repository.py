"""
Repository pattern implementation for database operations
"""

from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.infrastructure.db.database import Base
from app.infrastructure.db.models import UserProfileModel
from app.domain.entities.user_profile import UserProfile

ModelType = TypeVar("ModelType",bound=Base)

class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        instance = await self.get_by_id(id)
        if not instance:
            return None
        
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    async def delete(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if not instance:
            return False
        
        await self.db.delete(instance)
        await self.db.commit()
        return True
    
    async def exists(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        return instance is not None


class UserProfileRepository(BaseRepository[UserProfileModel]):
    """Repository for User Profile operations"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(UserProfileModel, db)
    
    async def get_by_phone_number(self, phone_number: str) -> Optional[UserProfileModel]:
        stmt = select(UserProfileModel).where(UserProfileModel.phone_number == phone_number)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def exists_by_phone_number(self, phone_number: str) -> bool:
        user = await self.get_by_phone_number(phone_number)
        return user is not None
    
    
    async def create_user_profile(self, user: UserProfile) -> UserProfileModel:
        """Create user from domain entity"""
        user_model = UserProfileModel(
            id = user.id,
            phone_number = user.phone_number,
            fullname = user.fullname,
            email = user.email,
            address = user.address,
            birthday_date = user.birthday_date,
            gender = user.gender,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.db.add(user_model)
        await self.db.commit()
        await self.db.refresh(user_model)
        return user_model