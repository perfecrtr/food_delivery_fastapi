from fastapi import APIRouter, status, Depends, Query
from pydantic import UUID4

from app.api.v1.schemas.deliveries import (
    GetDeliveryByIdResponse,
    GetCurrentDeliveryResponse,
    DeliveryInfo,
    UpdateDeliveryStatusRequest,
    UpdateDeliveryStatusResponse,
)
from app.application.commands.update_delivery_status import UpdateDeliveryStatusCommand, UpdateDeliveryStatusHandler
from app.application.queries.get_delivery_by_id import GetDeliveryByIdQuery, GetDeliveryByIdHandler
from app.application.queries.get_current_delivery import GetCurrentDeliveryQuery, GetCurrentDeliveryHandler
from app.core.dependencies import (
    get_delivery_getting_by_id_handler,
    get_current_delivery_getting_handler,
    get_current_user_id,
    get_delivery_status_updating_handler,
)

router = APIRouter(prefix="/deliveries", tags=["deliveries"])

@router.get("/me", response_model=GetCurrentDeliveryResponse, status_code=status.HTTP_200_OK)
async def get_current_delivery(
    current_user_id: int = Depends(get_current_user_id),
    handler: GetCurrentDeliveryHandler = Depends(get_current_delivery_getting_handler)
) -> GetCurrentDeliveryResponse:
    
    query = GetCurrentDeliveryQuery(
        auth_id = current_user_id
    )

    result = await handler.handle(query=query)

    return GetCurrentDeliveryResponse(
        delivery=DeliveryInfo(
            id=result.id,
            order_id=result.order_id,
            courier_id=result.courier_id,
            restaurant_address=result.restaurant_address.full_address,
            delivery_address=result.delivery_address.full_address,
            status=result.status.value,
            created_at=result.created_at,
            assigned_at=result.assigned_at,
            picked_up_at=result.picked_up_at,
            delivered_at=result.delivered_at,
            cancelled_at=result.cancelled_at,
            failed_at=result.failed_at,
            updated_at=result.updated_at,
        ) if result else None
    ) 

@router.get("/{delivery_id}", response_model=GetDeliveryByIdResponse, status_code=status.HTTP_200_OK)
async def get_delivery_by_id(
    delivery_id: UUID4,
    handler: GetDeliveryByIdHandler = Depends(get_delivery_getting_by_id_handler)
) -> GetDeliveryByIdResponse:
    
    query = GetDeliveryByIdQuery(
        delivery_id=delivery_id
    )

    result = await handler.handle(query=query)

    return GetDeliveryByIdResponse(
        delivery=DeliveryInfo(
            id=result.id,
            order_id=result.order_id,
            courier_id=result.courier_id,
            restaurant_address=result.restaurant_address.full_address,
            delivery_address=result.delivery_address.full_address,
            status=result.status.value,
            created_at=result.created_at,
            assigned_at=result.assigned_at,
            picked_up_at=result.picked_up_at,
            delivered_at=result.delivered_at,
            cancelled_at=result.cancelled_at,
            failed_at=result.failed_at,
            updated_at=result.updated_at,
        ) if result else None
    ) 

@router.patch("/{delivery_id}/status", response_model=UpdateDeliveryStatusResponse, status_code=status.HTTP_200_OK)
async def update_delivery_status(
    request: UpdateDeliveryStatusRequest, 
    delivery_id: UUID4,
    current_user_id: int = Depends(get_current_user_id),
    handler: UpdateDeliveryStatusHandler = Depends(get_delivery_status_updating_handler),
) -> UpdateDeliveryStatusResponse:
    
    command = UpdateDeliveryStatusCommand(
        delivery_id = delivery_id,
        new_status = request.new_status,
        auth_id = current_user_id,
    )

    result = await handler.handle(command=command)

    return UpdateDeliveryStatusResponse(
        delivery_id=result.delivery_id,
        new_status=result.new_status,
        msg=result.msg,
        updated_at=result.updated_at,

    )