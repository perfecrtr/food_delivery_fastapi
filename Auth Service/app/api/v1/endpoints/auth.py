"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.application.commands.register_user import RegisterUserCommand, RegisterUserHandler
from app.application.commands.login_user import UserLoginCommand, UserLoginHandler

from app.api.v1.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    ChangePasswordRequest,
    RefreshTokenRequest,
    TokenResponse
)
from app.core.dependencies import (
    get_password_hasher,
    get_token_service,
    get_user_repository,
    get_current_user_id,
    get_register_handler,
    get_login_handler
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
async def login(request: LoginRequest,
                   handler: UserLoginHandler = Depends(get_login_handler)):
    command = UserLoginCommand(phone_number=request.phone_number,
                               password=request.password)
    result = await handler.handle(command)
    return LoginResponse(
        access_token=result.get("access_token"),
        refresh_token=result.get("refresh_token")
    )
