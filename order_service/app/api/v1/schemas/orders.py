from pydantic import BaseModel, UUID4, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime

class OrderItemRequest(BaseModel):
    dish_id: UUID4
    quantity: int

    @field_validator('quantity')
    @classmethod
    def validate(cls, value):
        if value <= 0:
            raise ValueError('Quantity must be positive')
        return value
    
class AddressRequest(BaseModel):
    city: str
    street: str
    house_number: str
    apartment: Optional[str] = None 
    entrance: Optional[str] = None
    floor: Optional[str] = None

class CreateOrderRequest(BaseModel):
    restaurant_id: UUID4
    items: List[OrderItemRequest]
    delivery_address: AddressRequest
    payment_method: str
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "restaurant_id": "123e4567-e89b-12d3-a456-426614174000",
                "items": [
                    {
                        "dish_id": "987fcdeb-51a3-43b7-a456-426614174222",
                        "quantity": 2
                    },
                    {
                        "dish_id": "456abcde-89ab-4cde-b123-426614174333",
                        "quantity": 1
                    }
                ],
                "delivery_address": {
                    "city": "Минск",
                    "street": "Крутая",
                    "house_number": "8",
                    "apartment": "42",
                    "entrance": "2",
                    "floor": "5"
                }
            }
        }
    )


class CreateOrderResponse(BaseModel):
    id: UUID4
    status: str
    total_price: float
    message: str = "Order created successfully"

class OrderItemInfo(BaseModel):
    dish_id: UUID4
    name: str
    price: float
    quantity: int
    subtotal: float

class OrderInfo(BaseModel):
    id: UUID4
    items: List[OrderItemInfo]
    delivery_address: str
    restaurant_address: str
    total_price: float
    status: str

class GetOrdersRequest(BaseModel):
    page: int = 0
    per_page: int = 10

class GetOrdersResponse(BaseModel):
    orders: List[OrderInfo]

class CancelOrderRequest(BaseModel):
    order_id: UUID4

class CancelOrderResponse(BaseModel):
    order_id: UUID4
    cancelled_at: datetime
    msg: str

