"""
User Profile endpoints
"""

from fastapi import APIRouter, status, Depends, Path
from app.api.v1.schemas.users import (
    CreateUserProfileRequest,
    CreateUserProfileResponse,
    GetUserProfileResponse,
    UpdateUserProfileRequest, 
    UpdateUserProfileResponse
)
from app.application.commands.create_user_profile import CreateUserProfileCommand, CreateUserProfileHandler
from app.application.commands.update_user_profile import UpdateUserProfileCommand, UpdateUserProfileHandler
from app.application.queries.get_user_profile import GetUserProfileQuery, GetUserProfileHandler
from app.core.dependencies import get_creating_profile_handler, get_get_user_profile_handler, get_update_user_profile_handler

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

@router.get("/get/{user_id}", response_model=GetUserProfileResponse, status_code=status.HTTP_200_OK)
async def get_user_profile(
    user_id: int = Path(..., title="user id", gt=0),
    handler: GetUserProfileHandler = Depends(get_get_user_profile_handler)
):
    command = GetUserProfileQuery(id=user_id)
    result = await handler.handle(command)
    
    if result is None:
        raise

    return GetUserProfileResponse(**result)

@router.post("/user/{user_id}/update", response_model=UpdateUserProfileResponse, status_code=status.HTTP_200_OK)
async def update_user_profile(
    request: UpdateUserProfileRequest,
    handler: UpdateUserProfileHandler = Depends(get_update_user_profile_handler),
    user_id: int = Path(..., title="user id", gt=0),
):
    command = UpdateUserProfileCommand(id=user_id,
                                       fullname=request.fullname,
                                       email=request.email,
                                       address=request.address,
                                       birthday_date=request.birthday_date,
                                       gender=request.gender)
    
    result = await handler.handle(command)
    
    if result is None:
        raise

    return UpdateUserProfileResponse(**result)

