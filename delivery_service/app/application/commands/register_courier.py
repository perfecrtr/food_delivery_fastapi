from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime, timezone

from app.domain.value_objects import CourierStatus
from app.domain.enums import CourierStatusEnum
from app.domain.repositories.courier_repository import CourierRepository
from app.domain.services.user_service import UserService
from app.domain.entities.courier import Courier

@dataclass(frozen=True)
class RegisterCourierCommand:
    auth_id: int
    is_active: bool = True
    status: CourierStatus = CourierStatusEnum.OFFLINE

class RegisterCourierHandler:
    
    def __init__(
        self,
        repo: CourierRepository,
        user_service: UserService,
    ) -> None:
        self.repo = repo
        self.user_service = user_service

    async def handle(self, command: RegisterCourierCommand) -> Courier:
        user_service_response = await self.user_service.get_user_info(user_id=command.auth_id)

        courier = Courier(
            id=uuid4(),
            auth_id=command.auth_id,
            name=user_service_response.name,
            phone=user_service_response.phone,
            is_active=command.is_active,
            status=command.status,
            created_at=datetime.utcnow(),
        )

        result = await self.repo.create(courier)
        return result

