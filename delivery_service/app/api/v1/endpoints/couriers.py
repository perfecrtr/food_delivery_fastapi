from fastapi import APIRouter, status, Depends, Query

from app.api.v1.schemas.couriers import (
    RegisterCourierRequest,
    RegisterCourierResponse,
    UpdateCourierStatusRequest,
    UpdateCourierStatusResponse,
    GetAvailableCouriersRequest,
    GetAvailableCouriersResponse,
    CourierInfo,
)
from app.core.dependencies import (
    get_current_user_id,
    get_courier_registration_handler,
    get_courier_status_updating_handler,
    get_available_couriers_getting_handler,
)
from app.application.commands.register_courier import RegisterCourierCommand, RegisterCourierHandler
from app.application.commands.update_courier_status import UpdateCourierStatusCommand, UpdateCourierStatusHandler
from app.application.queries.get_available_couriers import GetAvailableCouriersQuery, GetAvailableCouriersHandler

router = APIRouter(prefix="/courier", tags=["couriers"])

@router.post("/", response_model=RegisterCourierResponse, status_code=status.HTTP_201_CREATED)
async def register_courier(
    request: RegisterCourierRequest,
    current_user_id: int = Depends(get_current_user_id),
    handler: RegisterCourierHandler = Depends(get_courier_registration_handler)
) -> RegisterCourierResponse:
    
    command = RegisterCourierCommand(
        auth_id=current_user_id
    )

    result = await handler.handle(command=command)

    return RegisterCourierResponse(
        id=result.id,
        auth_id=result.auth_id,
        name=result.name,
        phone=result.phone,
        is_active=result.is_active,
        status=result.status.value,
        created_at=result.created_at,
    )

@router.patch("/", response_model=UpdateCourierStatusResponse, status_code=status.HTTP_200_OK)
async def update_courier_status(
    request: UpdateCourierStatusRequest,
    current_user_id: int = Depends(get_current_user_id),
    handler: UpdateCourierStatusHandler = Depends(get_courier_status_updating_handler)
) -> UpdateCourierStatusResponse:
    
    command = UpdateCourierStatusCommand(
        auth_id=current_user_id,
        new_status=request.new_status,
    )

    result = await handler.handle(command=command)

    return UpdateCourierStatusResponse(
        id=result.courier_id,
        status=result.status,
        msg=result.msg,
        updated_at=result.updated_at,
    )

@router.get('/available', response_model=GetAvailableCouriersResponse, status_code=status.HTTP_200_OK)
async def get_available_couriers(
    request: GetAvailableCouriersRequest = Query(),
    handler: GetAvailableCouriersHandler = Depends(get_available_couriers_getting_handler)
) -> GetAvailableCouriersResponse:
    
    query = GetAvailableCouriersQuery(
        limit=request.limit,
    )
    
    result = await handler.handle(query=query)

    return GetAvailableCouriersResponse(
        couriers=[
            CourierInfo(
                id=courier.id,
                name=courier.name,
                phone=courier.phone,
                status=courier.status.value,
            ) for courier in result
        ] if result else None
    )
