"""
    API Schemas for menu categories operations restaurant service endpoint
"""

from pydantic import BaseModel
from uuid import UUID

class MenuCategoryInfo(BaseModel):
    id: UUID
    name: str

class CreateMenuCategoryRequest(BaseModel):
    name: str

class CreateMenuCategoryResonse(BaseModel):
    id: UUID
    msg: str

class GetMenuCategoriesRequest(BaseModel):
    page: int = 0
    per_page: int = 30

class GetMenuCategoriesResponse(BaseModel):
    categories: list[MenuCategoryInfo]
