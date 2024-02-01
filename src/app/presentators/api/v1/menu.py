import json
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.application.models.menu import (
    Menu,
    MenuCreate,
    MenuUpdatePatch,
    MenuUpdatePut,
    MenuWithoutSubmenus,
)
from app.domain.interfaces.usecases.menu import MenuUsecaseInterface
from app.infrastructure.cache.interface import CacheInterface

router = APIRouter(
    tags=['menu'],
    responses={
        404: {
            'description': 'Menu Not Found',
            'content': {
                'application/json': {
                    'example': {'detail': 'menu not found'},
                },
            },
        },
    },
)


@router.get(
    '/menus',
    response_model=list[Menu],
    status_code=200,
)
async def get_menus(
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = cache.get('menus')
    if not data:
        data = await menu_usecase.get_menus()
        data = jsonable_encoder(data)
        cache.set('menus', json.dumps(data), ex=30)
    else:
        data = json.loads(data)
    return data


@router.post(
    '/menus',
    response_model=MenuWithoutSubmenus,
    status_code=201,
)
async def create_menu(
    menu_data: MenuCreate,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = await menu_usecase.create_menu(menu_data.model_dump())
    cache.clear()
    return data


@router.get(
    '/menus/{menu_id}',
    response_model=MenuWithoutSubmenus,
    status_code=200,
)
async def get_menu(
    menu_id: UUID,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = cache.get(f'menu-{menu_id}')
    if not data:
        data = await menu_usecase.get_menu(menu_id)
        data = jsonable_encoder(data)
        cache.set(f'menu-{menu_id}', json.dumps(data), ex=30)
    else:
        data = json.loads(data)
    return data


@router.put(
    '/menus/{menu_id}',
    response_model=MenuWithoutSubmenus,
    status_code=200,
)
async def put_menu(
    menu_id: UUID,
    update_data: MenuUpdatePut,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = await menu_usecase.update_menu(
        menu_id,
        update_data.model_dump(exclude_none=True),
    )
    cache.delete('menus')
    cache.delete(f'menu-{menu_id}')
    return data


@router.patch(
    '/menus/{menu_id}',
    response_model=MenuWithoutSubmenus,
    status_code=200,
)
async def patch_menu(
    menu_id: UUID,
    update_data: MenuUpdatePatch,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = await menu_usecase.update_menu(
        menu_id,
        update_data.model_dump(exclude_none=True),
    )
    cache.delete('menus')
    cache.delete(f'menu-{menu_id}')
    return data


@router.delete(
    '/menus/{menu_id}',
    response_model=None,
    status_code=200,
)
async def delete_menu(
    menu_id: UUID,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> None:
    await menu_usecase.delete_menu(menu_id)
    cache.clear()
