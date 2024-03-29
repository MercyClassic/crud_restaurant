from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks

from app.application.models.dish import Dish, DishCreate, DishUpdatePatch, DishUpdatePut
from app.domain.interfaces.services.dish import DishServiceInterface
from app.infrastructure.cache.interfaces.dish import DishCacheServiceInterface

router = APIRouter(
    tags=['dish'],
    responses={
        404: {
            'description': 'Dish Not Found',
            'content': {
                'application/json': {
                    'example': {'detail': 'dish not found'},
                },
            },
        },
    },
)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['GET'],
    response_model=list[Dish],
    status_code=200,
)
async def get_dishes(
    dish_usecase: Annotated[DishServiceInterface, Depends()],
) -> Any:
    data = await dish_usecase.get_dishes()
    return data


@router.post(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['POST'],
    response_model=Dish,
    status_code=201,
)
async def create_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_data: DishCreate,
    dish_usecase: Annotated[DishServiceInterface, Depends()],
    dish_cache_service: Annotated[DishCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> Any:
    data = await dish_usecase.create_dish(
        submenu_id=submenu_id,
        title=dish_data.title,
        description=dish_data.description,
        price=dish_data.price,
    )
    background_tasks.add_task(
        dish_cache_service.invalidate_cache_after_create_dish,
        menu_id,
        submenu_id,
    )
    return data


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    tags=['GET'],
    response_model=Dish,
    status_code=200,
)
async def get_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_usecase: Annotated[DishServiceInterface, Depends()],
) -> Any:
    data = await dish_usecase.get_dish(dish_id, submenu_id, menu_id)
    return data


@router.put(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    tags=['PUT'],
    response_model=Dish,
    status_code=200,
)
async def put_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    update_data: DishUpdatePut,
    dish_usecase: Annotated[DishServiceInterface, Depends()],
    dish_cache_service: Annotated[DishCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> Any:
    data = await dish_usecase.update_dish(
        dish_id,
        title=update_data.title,
        description=update_data.description,
        price=update_data.price,
    )
    background_tasks.add_task(
        dish_cache_service.invalidate_cache_after_update_dish,
        dish_id,
        menu_id,
        submenu_id,
    )
    return data


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    tags=['PATCH'],
    response_model=Dish,
    status_code=200,
)
async def patch_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    update_data: DishUpdatePatch,
    dish_usecase: Annotated[DishServiceInterface, Depends()],
    dish_cache_service: Annotated[DishCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> Any:
    data = await dish_usecase.update_dish(
        dish_id=dish_id,
        title=update_data.title,
        description=update_data.description,
        price=update_data.price,
    )
    background_tasks.add_task(
        dish_cache_service.invalidate_cache_after_update_dish,
        dish_id,
        submenu_id,
        menu_id,
    )
    return data


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    tags=['DELETE'],
    response_model=None,
    status_code=200,
)
async def delete_dish(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_usecase: Annotated[DishServiceInterface, Depends()],
    dish_cache_service: Annotated[DishCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> None:
    await dish_usecase.delete_dish(
        dish_id=dish_id,
    )
    background_tasks.add_task(
        dish_cache_service.invalidate_cache_after_delete_dish,
        dish_id,
        submenu_id,
        menu_id,
    )
