"""
Repository pattern implementation for database operations
Async version using SQLAlchemy 2.0 async API
"""

from typing import Optional, Type, TypeVar, Generic, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from app.infrastructure.db.database import Base
from app.infrastructure.db.models import UserModel

ModelType = TypeVar("ModelType", bound=Base)


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


class UserRepository(BaseRepository[UserModel]):
    """Repository for User operations"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(UserModel, db)
    
    async def get_by_phone_number(self, phone_number: str) -> Optional[UserModel]:
        stmt = select(UserModel).where(UserModel.phone_number == phone_number)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def exists_by_phone_number(self, phone_number: str) -> bool:
        user = await self.get_by_phone_number(phone_number)
        return user is not None
    
    async def update_last_login(self, user_id: int) -> Optional[UserModel]:
        from datetime import datetime
        return await self.update(user_id, last_login=datetime.utcnow())
    
    async def update_password(self, user_id: int, hashed_password: str) -> Optional[UserModel]:
        return await self.update(user_id, hashed_password=hashed_password)
    
    async def create_user(self, user: Any) -> UserModel:
        """Create user from domain entity"""
        user_model = UserModel(
            phone_number=user.phone_number,
            hashed_password=user.password_hash,
            full_name=user.full_name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.db.add(user_model)
        await self.db.commit()
        await self.db.refresh(user_model)
        return user_model