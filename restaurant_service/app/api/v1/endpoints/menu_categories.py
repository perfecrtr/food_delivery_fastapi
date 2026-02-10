from fastapi import APIRouter, status, Depends, Query
from app.api.v1.schemas.menu_categories import (
    CreateMenuCategoryRequest,
    CreateMenuCategoryResonse,
    GetMenuCategoriesRequest,
    GetMenuCategoriesResponse
)
from app.application.commands.create_menu_category import CreateMenuCategoryCommand, CreateMenuCategoryHandler
from app.application.queries.get_menu_categories import GetMenuCategoriesQuery, GetMenuCategoriesHandler
from app.core.dependencies import get_menu_category_creating_handler, get_menu_categories_getting_handler

router = APIRouter(prefix="/menu_categories", tags=["menu_categories"])

@router.post("/", response_model=CreateMenuCategoryResonse, status_code=status.HTTP_201_CREATED)
async def create_menu_category(
    request: CreateMenuCategoryRequest,
    handler: CreateMenuCategoryHandler = Depends(get_menu_category_creating_handler)
) -> CreateMenuCategoryResonse:
    
    command = CreateMenuCategoryCommand(
        name = request.name
    )

    result = await handler.handle(command)
    return CreateMenuCategoryResonse(**result)

@router.get("/", response_model=GetMenuCategoriesResponse, status_code=status.HTTP_200_OK)
async def get_restraunts(
    request: GetMenuCategoriesRequest = Query(),
    handler: GetMenuCategoriesHandler = Depends(get_menu_categories_getting_handler)
) -> GetMenuCategoriesResponse:
    
    command = GetMenuCategoriesQuery(
        page=request.page,
        per_page=request.per_page
    )

    result = await handler.handle(command)
    
    if result is None:
        raise

    return GetMenuCategoriesResponse(categories=result)