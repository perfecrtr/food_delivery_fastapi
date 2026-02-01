"""
Repository pattern implementation for database operations
"""

from typing import Optional, Type, TypeVar, Generic, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.infrastructure.db.database import Base
from app.infrastructure.db.models import UserModel

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: int, **kwargs) -> Optional[ModelType]:
 
        instance = self.get_by_id(id)
        if not instance:
            return None
        
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if not instance:
            return False
        
        self.db.delete(instance)
        self.db.commit()
        return True
    
    def exists(self, id: int) -> bool:
        return self.db.query(self.model).filter(self.model.id == id).first() is not None


class UserRepository(BaseRepository[UserModel]):
    """Repository for User operations"""
    
    def __init__(self, db: Session):
        super().__init__(UserModel, db)
    
    def get_by_phone_number(self, phone_number: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(
            UserModel.phone_number == phone_number
        ).first()
    
    def exists_by_phone_number(self, phone_number: str) -> bool:
        return self.get_by_phone_number(phone_number) is not None
    
    def update_last_login(self, user_id: int) -> Optional[UserModel]:
        from datetime import datetime
        return self.update(user_id, last_login=datetime.utcnow())
    
    def update_password(self, user_id: int, hashed_password: str) -> Optional[UserModel]:
        return self.update(user_id, hashed_password=hashed_password)
