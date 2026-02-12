from enum import Enum

class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"