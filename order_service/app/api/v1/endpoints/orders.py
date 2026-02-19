from fastapi import APIRouter, Depends, status, Query, Request, HTTPException
import hashlib
from app.api.v1.schemas.orders import (
    CreateOrderRequest,
    CreateOrderResponse,
    GetOrdersRequest,
    GetOrdersResponse,
    OrderItemInfo,
    OrderInfo,
    CancelOrderRequest,
    CancelOrderResponse
)
from app.application.commands.create_order import CreateOrderCommand, CreateOrderHandler
from app.application.commands.cancel_order import CancelOrderCommand, CancelOrderHandler
from app.application.queries.get_orders import GetOrdersQuery, GetOrdersHandler
from app.domain.services.idempotency_service import IdempotencyService
from app.core.dependecies import(
    get_current_user_id,
    get_order_creating_handler,
    get_order_getting_handler,
    get_order_cancelling_handler,
     get_idempotency_service
)
from uuid import UUID

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=CreateOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    request_head: Request,
    request: CreateOrderRequest,
    current_user_id: int = Depends(get_current_user_id),
    handler: CreateOrderHandler = Depends(get_order_creating_handler),
    idemp: IdempotencyService = Depends(get_idempotency_service)
) -> CreateOrderResponse:
    
    idempotency_key = request_head.headers.get("Idempotency-Key")
    if not idempotency_key:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Idempotency-Key header is required")
    
    payload = request.model_dump_json()
    fingerprint_src = f"{request_head.method}:{request_head.url.path}:{payload}"
    fingerprint = hashlib.sha256(fingerprint_src.encode()).hexdigest()
    
    async def action() -> dict:
        command = CreateOrderCommand(
            restaurant_id=request.restaurant_id,
            user_id=current_user_id,
            delivery_address=request.delivery_address.model_dump(),
            items=[
                {"dish_id": item.dish_id, "quantity": item.quantity}
                for item in request.items
            ],
            payment_method=request.payment_method
        )
        result = await handler.handle(command=command)

        return {
            "id": result.id,
            "status": result.status.value,
            "total_price": result.total_price.amount,
            "message": "Order created successfully",
        }

    data = await idemp.run(
        key=idempotency_key,
        fingerprint=fingerprint,
        action=action,
    )

    return CreateOrderResponse(**data)

@router.get("/my", response_model=GetOrdersResponse, status_code=status.HTTP_200_OK)
async def get_user_orders(
    request: GetOrdersRequest = Query(),
    current_user_id: int = Depends(get_current_user_id),
    handler: GetOrdersHandler = Depends(get_order_getting_handler)
) -> GetOrdersResponse:
    
    query = GetOrdersQuery(
        user_id=current_user_id,
        page=request.page,
        per_page=request.per_page
    )

    result = await handler.handle(query=query)

    return GetOrdersResponse(
        orders=[
            OrderInfo(
                id=order.id,
                delivery_address=order.delivery_address.full_address,
                total_price=order.total_price.amount,
                status=order.status.value,
                items= [
                    OrderItemInfo(
                        dish_id=item.dish_id,
                        name=item.name,
                        price=item.price.amount,
                        quantity=item.quantity,
                        subtotal=item.total.amount
                    ) for item in order.items
                ]
            )
            for order in result
        ]
    )

@router.patch("/{order_id}/cancel", response_model=CancelOrderResponse, status_code=status.HTTP_200_OK)
async def cancel_order(
    request: CancelOrderRequest = Query,
    current_user_id: int = Depends(get_current_user_id),
    handler: CancelOrderHandler = Depends(get_order_cancelling_handler)
) -> CancelOrderResponse:
    
    command = CancelOrderCommand(
        order_id=request.order_id,
        user_id=current_user_id
    )

    result = await handler.handle(command=command)

    return CancelOrderResponse(
        order_id=result.order_id,
        cancelled_at=result.cancelled_at,
        msg=result.message
    )