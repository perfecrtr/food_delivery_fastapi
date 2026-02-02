"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.exc import IntegrityError

from app.application.commands.register_user import RegisterUserCommand, RegisterUserHandler
from app.application.commands.login_user import UserLoginCommand, UserLoginHandler
from app.application.commands.change_password import UserChangePasswordCommand, UserChangePasswordHandler
from app.infrastructure.redis.rate_limiter import RateLimiter
from app.infrastructure.redis.token_store import TokenStore
from datetime import datetime

from app.api.v1.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    LogoutRequest,
    LogoutResponse
)
from app.core.dependencies import (
    get_register_handler,
    get_login_handler,
    get_change_password_handler,
    get_redis,
    get_login_rate_limiter,
    get_token_service,
    get_token_store,
    security
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
    rate_limiter: RateLimiter = Depends(get_login_rate_limiter),
    token_service: TokenService = Depends(get_token_service),
    token_store: TokenStore = Depends(get_token_store)
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

    refresh_token_str = result.get("refresh_token")
    payload = token_service.verify_refresh_token(refresh_token_str)
    user_id = payload.get("user_id")
    sid = payload.get("sid")

    if user_id and sid:
        await token_store.save_refresh_session(sid, user_id)

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

@router.post("/refresh", response_model=RefreshTokenResponse, status_code=status.HTTP_200_OK)
async def refresh_tokens(
    request: RefreshTokenRequest,
    token_service: TokenService = Depends(get_token_service),
    token_store: TokenStore = Depends(get_token_store)
    ):

    try:
        payload = token_service.verify_refresh_token(request.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = str(e)
        )
    
    user_id = payload.get("user_id")
    sid = payload.get("sid")

    if not user_id or not sid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload",
        )

    session_user_id = await token_store.get_refresh_session(sid)
    if session_user_id is None or session_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh session is invalid or expired",
        )
    
    access_token_vo = token_service.generate_access_token(user_id)
    new_refresh_vo = token_service.generate_refresh_token(user_id)

    new_refresh_payload = token_service.verify_refresh_token(str(new_refresh_vo))
    new_sid = new_refresh_payload.get("sid")
    if not new_sid:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate refresh session id",
        )
    
    await token_store.rotate_refresh_session(
        old_sid=sid,
        new_sid=new_sid,
        user_id=user_id,
    )

    return RefreshTokenResponse(
        access_token=str(access_token_vo),
        refresh_token=str(new_refresh_vo),
        token_type="bearer",
    )

@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
async def logout(
    request: LogoutRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_service: TokenService = Depends(get_token_service),
    token_store: TokenStore = Depends(get_token_store),
):
    
    access_token = credentials.credentials

    try:
        access_payload = token_service.verify_access_token(access_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    jti = access_payload.get("jti")
    exp = access_payload.get("exp")

    ttl_seconds = None
    if isinstance(exp, datetime):
        remaining = int((exp - datetime.utcnow()).total_seconds())
        ttl_seconds = max(1, remaining)

    if jti:
        await token_store.blacklist_access_token(jti, ttl_seconds)

    if request.refresh_token:
        try:
            refresh_payload = token_service.verify_refresh_token(request.refresh_token)
            sid = refresh_payload.get("sid")
            if sid:
                await token_store.delete_refresh_session(sid)
        except ValueError:
            pass

    return LogoutResponse(
        success=True,
        message="Logged out successfully",
    )