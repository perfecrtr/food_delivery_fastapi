from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.application.commands.create_restaurant import CreateRestaurantHandler
from app.application.commands.create_menu_category import CreateMenuCategoryHandler
from app.application.commands.create_dish import CreateDishHandler
from app.application.commands.update_restaurant import UpdateRestaurantHandler
from app.application.commands.update_dish import UpdateDishHandler
from app.application.queries.get_restraunts import GetAllRestrauntsHandler
from app.application.queries.get_menu_categories import GetMenuCategoriesHandler
from app.application.queries.get_restraunt_menu import GetRestaurantMenuHandler
from app.application.queries.get_restraunt import GetRestaurantHandler
from app.infrastructure.db.database import get_db
from app.infrastructure.db.repositories.restaurant_repository import SQLAlchemyRestaurantRepository
from app.infrastructure.db.repositories.menu_category_repository import SQLAlchemyMenuCategoryRepository
from app.infrastructure.db.repositories.dish_repository import SQLAlchemyDishRepository
from app.infrastructure.db.repositories.menu_repository import SQLAlchemyMenuRepository


async def get_restaurant_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyRestaurantRepository:
    """
    Get user repository instance
    """
    return SQLAlchemyRestaurantRepository(db)

async def get_menu_category_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyMenuCategoryRepository:
    """
    Get user repository instance
    """
    return SQLAlchemyMenuCategoryRepository(db)

async def get_dish_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyDishRepository:
    return SQLAlchemyDishRepository(db)

async def get_menu_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyMenuRepository:
    return SQLAlchemyMenuRepository(db)

async def get_creating_restaurant_handler(restaurant_repository = Depends(get_restaurant_repository)):
    return(
        CreateRestaurantHandler(
            restaurant_repository
        )
    )

async def get_getting_all_restaurants_handler(restaurant_repository = Depends(get_restaurant_repository)):
    return(
        GetAllRestrauntsHandler(
            restaurant_repository
        )
    )

async def get_restaurant_getting_handler(restaurant_repository = Depends(get_restaurant_repository)):
    return(
        GetRestaurantHandler(
            restaurant_repository
        )
    )

async def get_updating_restaurant_handler(restaurant_repository = Depends(get_restaurant_repository)):
    return(
        UpdateRestaurantHandler(
            restaurant_repository
        )
    )

async def get_restaurant_menu_getting_handler(repo = Depends(get_menu_repository)):
    return(
        GetRestaurantMenuHandler(
            repo
        )
    )

async def get_menu_category_creating_handler(menu_category_repository = Depends(get_menu_category_repository)):
    return(
        CreateMenuCategoryHandler(
            menu_category_repository
        )
    )

async def get_menu_categories_getting_handler(menu_category_repository = Depends(get_menu_category_repository)):
    return(
        GetMenuCategoriesHandler(
            menu_category_repository
        )
    )

async def get_dish_creating_handler(dish_repository = Depends(get_dish_repository)):
    return(
        CreateDishHandler(
            dish_repository
        )
    )

async def get_dish_updating_handler(dish_repository = Depends(get_dish_repository)):
    return(
        UpdateDishHandler(
            dish_repository
        )
    )