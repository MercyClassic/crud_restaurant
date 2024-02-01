import json
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.application.models.dish import Dish, DishCreate, DishUpdatePatch, DishUpdatePut
from app.domain.interfaces.usecases.dish import DishUsecaseInterface
from app.infrastructure.cache.interface import CacheInterface

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
    response_model=list[Dish],
    status_code=200,
)
async def get_dishes(
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = cache.get('dishes')
    if not data:
        data = await dish_usecase.get_dishes()
        data = jsonable_encoder(data)
        cache.set('dishes', json.dumps(data), ex=30)
    else:
        data = json.loads(data)
    return data


@router.post(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=Dish,
    status_code=201,
)
async def create_dish(
    submenu_id: UUID,
    dish_data: DishCreate,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = await dish_usecase.create_dish(submenu_id, dish_data.model_dump())
    cache.clear()
    return data


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish,
    status_code=200,
)
async def get_dish(
    dish_id: UUID,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = cache.get(f'dish-{dish_id}')
    if not data:
        data = await dish_usecase.get_dish(dish_id)
        data = jsonable_encoder(data)
        cache.set(f'dish-{dish_id}', json.dumps(data), ex=30)
    else:
        data = json.loads(data)
    return data


@router.put(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish,
    status_code=200,
)
async def put_dish(
    dish_id: UUID,
    update_data: DishUpdatePut,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = await dish_usecase.update_dish(dish_id, update_data.model_dump(exclude_none=True))
    cache.delete('dishes')
    cache.delete(f'dish-{dish_id}')
    return data


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=Dish,
    status_code=200,
)
async def patch_dish(
    dish_id: UUID,
    update_data: DishUpdatePatch,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = await dish_usecase.update_dish(dish_id, update_data.model_dump(exclude_none=True))
    cache.delete('dishes')
    cache.delete(f'dish-{dish_id}')
    return data


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=None,
    status_code=200,
)
async def delete_dish(
    dish_id: UUID,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> None:
    await dish_usecase.delete_dish(dish_id)
    cache.clear()
