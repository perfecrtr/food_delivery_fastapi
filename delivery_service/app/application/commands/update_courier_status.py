from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.domain.enums import CourierStatusEnum
from app.domain.repositories.courier_repository import CourierRepository

@dataclass(frozen=True)
class UpdateCourierStatusCommand:
    auth_id: int
    new_status: CourierStatusEnum

@dataclass(frozen=True)
class UpdateCourierStatusResult:
    courier_id: UUID
    status: CourierStatusEnum
    msg: str
    updated_at: Optional[datetime]

class UpdateCourierStatusHandler:
    def __init__(
        self,
        repo: CourierRepository
    ) -> None:
        self.repo = repo

    async def handle(self, command: UpdateCourierStatusCommand) -> UpdateCourierStatusResult:
        courier = await self.repo.get_by_auth_id(auth_id=command.auth_id)
        if not courier:
            raise ValueError(f"Courier with auth_id {command.auth_id} not found")

        if courier.status.value == command.new_status:
            return UpdateCourierStatusResult(
                courier_id=courier.id,
                status=courier.status.value,
                msg="Status already set to requested value!",
                updated_at=courier.updated_at
            )
        
        if command.new_status == CourierStatusEnum.AVAILABLE and courier.status.value == CourierStatusEnum.OFFLINE:
            courier.go_online()
        elif command.new_status == CourierStatusEnum.AVAILABLE and courier.status.value == CourierStatusEnum.ON_BREAK:
            courier.end_break()
        elif command.new_status == CourierStatusEnum.OFFLINE:
            courier.go_offline()
        elif command.new_status == CourierStatusEnum.ON_BREAK:
            courier.take_break()

        updated_courier = await self.repo.update(courier)

        return UpdateCourierStatusResult(
            courier_id=updated_courier.id,
            status=updated_courier.status.value,
            msg="Status successfully updated!",
            updated_at=updated_courier.updated_at,
        )