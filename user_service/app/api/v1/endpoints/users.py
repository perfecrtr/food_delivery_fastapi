"""
User Profile endpoints
"""

from fastapi import APIRouter, status, Depends
from app.api.v1.schemas.users import (
    CreateUserProfileRequest,
    CreateUserProfileResponse
)
from app.application.commands.create_user_profile import CreateUserProfileCommand, CreateUserProfileHandler
from app.core.dependencies import get_creating_profile_handler

router = APIRouter(prefix="/user", tags=["user_profile"])

@router.post("/create", response_model=CreateUserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(request: CreateUserProfileRequest,
                              handler: CreateUserProfileHandler = Depends(get_creating_profile_handler)):
    command = CreateUserProfileCommand(id=request.id,
                                       phone_number=request.phone_number,
                                       fullname = request.fullname)
    
    result = await handler.handle(command)
    return CreateUserProfileResponse(
        id=result.get("id"),
        phone_number=result.get("phone_number"),
        fullname=result.get("fullname"),
        msg="User profile created successfully!"
    )