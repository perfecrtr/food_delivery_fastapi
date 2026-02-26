from dataclasses import dataclass
from uuid import UUID
import random
import asyncio

from app.domain.services.courier_assignment import CourierAssignment, AssignmentResult
from app.domain.repositories.courier_repository import CourierRepository
from app.domain.repositories.delivery_repository import DeliveryRepository
from app.domain.enums import DeliveryStatusEnum
from app.domain.entities.delivery import Delivery
from app.domain.entities.courier import Courier

@dataclass
class RetryConfig:
    max_retries: int = 3
    initial_delay: float = 2.0
    max_delay: float = 5.0
    backoff_multiplier: float = 2.0

class SimpleRandomCourierAssignment(CourierAssignment):

    def __init__(self,
        courier_repo: CourierRepository,
        delivery_repo: DeliveryRepository,
        retry_config: RetryConfig = None
    ):
        self.courier_repo = courier_repo
        self.delivery_repo = delivery_repo
        self.retry_config = retry_config or RetryConfig()

    async def assign_to_delivery(self, delivery_id: UUID) -> AssignmentResult:
        delivery = await self.delivery_repo.get_by_id(delivery_id=delivery_id)
        if not delivery:
            return AssignmentResult(
                success=False,
                message=f"Delivery {delivery_id} not found"
            )
        
        precheck_result = await self._precheck_delivery(delivery=delivery)
        if not precheck_result.success:
            return precheck_result
        
        last_error=""

        for attempt in range(1, self.retry_config.max_retries + 1):

            result = await self._try_assign(delivery)

            if result.success:
                return result
            
            last_error = result.message

            if attempt < self.retry_config.max_retries:
                delay = self._calculate_delay(attempt=attempt)
                await asyncio.sleep(delay=delay)

        return AssignmentResult(
            success=False,
            delivery_id=delivery_id,
            message=f"All {self.retry_config.max_retries} attempts failed. Last error: {last_error}"
        )


    async def _precheck_delivery(self, delivery: Delivery) -> AssignmentResult:
        if delivery.courier_id is not None:
            return AssignmentResult(
                success=False,
                delivery_id=delivery.id,
                courier_id=delivery.courier_id,
                message=f"Delivery already has courier assigned"
            )

        if delivery.status.value != DeliveryStatusEnum.PENDING:
            return AssignmentResult(
                success=False,
                delivery_id=delivery.id,
                message=f"Delivery in status {delivery.status.value} cannot be assigned"
            )
        
        return AssignmentResult(success=True)
    
    async def _try_assign(self, delivery: Delivery) -> AssignmentResult:
        try:
            fresh_delivery = await self.delivery_repo.get_by_id(delivery.id)
            if not fresh_delivery:
                return AssignmentResult(
                    success=False,
                    message=f"Delivery {delivery.id} not found"
                )
            
            if fresh_delivery.courier_id is not None:
                return AssignmentResult(
                    success=False,
                    delivery_id=delivery.id,
                    courier_id=fresh_delivery.courier_id,
                    message="Delivery was assigned by another process"
                )
            
            available_couriers = await self.courier_repo.find_available()
            
            if not available_couriers:
                return AssignmentResult(
                    success=False,
                    delivery_id=delivery.id,
                    message="No available couriers at this moment"
                )
            
            selected_courier = random.choice(available_couriers)

            return await self._execute_assignment(
                delivery=fresh_delivery,
                courier=selected_courier,
            )

        except Exception as e:
            return AssignmentResult(
                success=False,
                delivery_id=delivery.id,
                message=f"Assignment error: {str(e)}"
            )
        
    async def _execute_assignment(
        self, 
        delivery: Delivery,
        courier: Courier,
    ) -> AssignmentResult:
        fresh_courier = await self.courier_repo.get_by_id(courier_id=courier.id)

        if not fresh_courier or not fresh_courier.is_available:
            return AssignmentResult(
                success=False,
                delivery_id=delivery.id,
                message=f"Courier {courier.id} is no longer available"
            )
        
        try:
            delivery.assign_courier(courier.id)
            await self.delivery_repo.update(delivery)
            
            courier.assign_to_delivery()
            await self.courier_repo.update(courier)
            
            return AssignmentResult(
                success=True,
                delivery_id=delivery.id,
                courier_id=courier.id,
                message=f"Courier {courier.name} assigned successfully"
            )
            
        except Exception as e:
            return AssignmentResult(
                success=False,
                delivery_id=delivery.id,
                message=f"Assignment failed: {str(e)}"
            )
        
    def _calculate_delay(self, attempt: int) -> float:
        delay = self.retry_config.initial_delay * (self.retry_config.backoff_multiplier ** (attempt - 1))

        jitter = random.uniform(0.8, 1.2)
        delay = delay * jitter

        return min(delay, self.retry_config.max_delay)
        