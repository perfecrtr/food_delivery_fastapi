import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from uuid import UUID
from typing import List, Dict, Any

from app.domain.services.restaurant_service import RestaurantService, ValidationResult, ValidatedItem
from app.core.config import settings

class RestaurantServiceHttpAdapter(RestaurantService):

    def __init__(
        self,
        base_url: str = settings.restaurant_service_url,
        timeout: int = settings.services_timeout,
        max_retries: int = settings.service_max_retries
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_keepalive_connections=10),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Order-Service/1.0"
            }
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError
        ))
    )
    async def validate_order_items(
        self,
        restaurant_id: UUID,
        items: List[Dict[str, Any]]
    ) -> ValidationResult:
        try:
            url = f"/api/v1/restaurant/{restaurant_id}/validate"
            payload = {
                "items": [
                    {
                        "dish_id": str(item["dish_id"]),
                        "quantity": item["quantity"]
                    }
                    for item in items
                ]
            }

            response = await self.client.post(url, json=payload)

            if response.status_code == 200:
                return self._parse_success_response(response.json())
            else: 
                return ValidationResult(
                    restaurant_address=None,
                    is_valid=False,
                    validated_items=[],
                    errors=[{
                        "code": "HTTP_ERROR",
                        "message": f"Restaurant service returned {response.status_code}"
                    }]
                )
            
        except httpx.TimeoutException:
            return ValidationResult(
                restaurant_address=None,
                is_valid=False,
                validated_items=[],
                errors=[{
                    "code": "SERVICE_TIMEOUT",
                    "message": "Restaurant service timeout"
                }]
            )
        except Exception as e:
            return ValidationResult(
                restaurant_address=None,
                is_valid=False,
                validated_items=[],
                errors=[{
                    "code": "INTERNAL_ERROR",
                    "message": f"Internal error: {str(e)}"
                }]
            )
        
    def _parse_success_response(self, data: Dict[str, Any]) -> ValidationResult:
        
        validated_items = []
        for item in data.get("validated_items", []):
            validated_items.append(ValidatedItem(
                dish_id=UUID(item["dish_id"]),
                name=item["name"],
                price=float(item["price"]),
                quantity=int(item["quantity"])
            ))
        
        return ValidationResult(
            restaurant_address=data.get("restaurant_address"),
            is_valid=data.get("is_valid", False),
            validated_items=validated_items,
            errors=data.get("errors", [])
        )