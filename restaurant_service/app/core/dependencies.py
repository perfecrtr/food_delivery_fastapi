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
from app.infrastructure.db.database import get_db
from app.infrastructure.db.repository import RestaurantRepository, MenuCategoryRepository, DishRepository



async def get_restaurant_repository(db: AsyncSession = Depends(get_db)) -> RestaurantRepository:
    """
    Get user repository instance
    """
    return RestaurantRepository(db)

async def get_menu_category_repository(db: AsyncSession = Depends(get_db)) -> MenuCategoryRepository:
    """
    Get user repository instance
    """
    return MenuCategoryRepository(db)

async def get_dish_repository(db: AsyncSession = Depends(get_db)) -> DishRepository:
    return DishRepository(db)

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

async def get_updating_restaurant_handler(restaurant_repository = Depends(get_restaurant_repository)):
    return(
        UpdateRestaurantHandler(
            restaurant_repository
        )
    )

async def get_restaurant_menu_getting_handler(dish_repository = Depends(get_dish_repository)):
    return(
        GetRestaurantMenuHandler(
            dish_repository
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