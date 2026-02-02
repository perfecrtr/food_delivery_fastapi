"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.exc import IntegrityError

from app.application.commands.register_user import RegisterUserCommand, RegisterUserHandler
from app.application.commands.login_user import UserLoginCommand, UserLoginHandler
from app.application.commands.change_password import UserChangePasswordCommand, UserChangePasswordHandler
from app.infrastructure.redis.rate_limiter import RateLimiter

from app.api.v1.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    ChangePasswordRequest,
    ChangePasswordResponse
)
from app.core.dependencies import (
    get_register_handler,
    get_login_handler,
    get_change_password_handler,
    get_redis,
    get_login_rate_limiter
)
from app.domain.services.password_hasher import PasswordHasher
from app.domain.services.token_service import TokenService
from app.domain.value_objects.password import Password
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.db.repository import UserRepository
from app.infrastructure.db.models import UserModel

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest,
                   handler: RegisterUserHandler = Depends(get_register_handler)):
    command = RegisterUserCommand(phone_number=request.phone_number,
                                  password=request.password,
                                  full_name=request.full_name)
    user, tokens = await handler.handle(command)
    return RegisterResponse(
        user_id = user.id,
        created_at = user.created_at
    )


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    http_request: Request,
    handler: UserLoginHandler = Depends(get_login_handler),
    rate_limiter: RateLimiter = Depends(get_login_rate_limiter)
    ):

    client_ip = http_request.client.host if http_request.client else "unknown"
    identity = f"{request.phone_number}:{client_ip}"

    allowed = await rate_limiter.is_allowed(scope="login", identity=identity)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )
    
    command = UserLoginCommand(phone_number=request.phone_number,
                               password=request.password)
    result = await handler.handle(command)
    return LoginResponse(
        access_token=result.get("access_token"),
        refresh_token=result.get("refresh_token")
    )


@router.put("/change_password", response_model=ChangePasswordResponse, status_code=status.HTTP_200_OK)
async def change_password(request : ChangePasswordRequest,
                          handler : UserChangePasswordHandler = Depends(get_change_password_handler)):
    command = UserChangePasswordCommand(phone = request.phone_number,
                                        old_password= request.old_password,
                                        new_password= request.new_password)
    result = await handler.handle(command)
    return ChangePasswordResponse(
        success = result.get("success"),
        message = result.get("message"),
        user_id = result.get("user_id")
    )
