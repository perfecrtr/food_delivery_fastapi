import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from uuid import UUID
from typing import List, Dict, Any

from app.domain.services.user_service import UserService, UserServiceResponse
from app.core.config import settings

class UserServiceHttpAdapter(UserService):

    def __init__(
        self,
        base_url: str = settings.user_service_url,
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
                "User-Agent": "Delivery-Service/1.0"
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
    async def get_user_info(
        self,
        user_id: int,
    ) -> UserServiceResponse:
        try:
            url = f"/api/v1/user/user/{user_id}"

            response = await self.client.get(url)

            if response.status_code == 200:
                return self._parse_success_response(response.json())
            else: 
                return None
            
        except httpx.TimeoutException:
            return None
        except Exception as e:
            return None
        
    def _parse_success_response(self, data: Dict[str, Any]) -> UserServiceResponse:
        
        return UserServiceResponse(
            phone=data.get("phone_number"),
            name=data.get("fullname"),
        )