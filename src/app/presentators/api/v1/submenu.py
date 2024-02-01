import json
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.application.models.submenu import (
    Submenu,
    SubmenuCreate,
    SubmenuUpdatePatch,
    SubmenuUpdatePut,
    SubmenuWithDishCount,
)
from app.domain.interfaces.usecases.submenu import SubmenuUsecaseInterface
from app.infrastructure.cache.interface import CacheInterface

router = APIRouter(
    tags=['submenu'],
    responses={
        404: {
            'description': 'Submenu Not Found',
            'content': {
                'application/json': {
                    'example': {'detail': 'submenu not found'},
                },
            },
        },
    },
)


@router.get(
    '/menus/{menu_id}/submenus',
    response_model=list[SubmenuWithDishCount],
    status_code=200,
)
async def get_submenus(
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = cache.get('submenus')
    if not data:
        data = await submenu_usecase.get_submenus()
        data = jsonable_encoder(data)
        cache.set('submenus', json.dumps(data), ex=30)
    else:
        data = json.loads(data)
    return data


@router.post(
    '/menus/{menu_id}/submenus',
    response_model=Submenu,
    status_code=201,
)
async def create_submenu(
    menu_id: UUID,
    submenu_data: SubmenuCreate,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = await submenu_usecase.create_submenu(menu_id, submenu_data.model_dump())
    cache.clear()
    return data


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuWithDishCount,
    status_code=200,
)
async def get_submenu(
    submenu_id: UUID,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = cache.get(f'submenu-{submenu_id}')
    if not data:
        data = await submenu_usecase.get_submenu(submenu_id)
        data = jsonable_encoder(data)
        cache.set(f'submenu-{submenu_id}', json.dumps(data), ex=30)
    else:
        data = json.loads(data)
    return data


@router.put(
    '/menus/{menu_id}/submenus/{submenu_id}',
    response_model=Submenu,
    status_code=200,
)
async def put_submenu(
    submenu_id: UUID,
    update_data: SubmenuUpdatePut,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = await submenu_usecase.update_submenu(
        submenu_id,
        update_data.model_dump(exclude_none=True),
    )
    cache.delete('submenus')
    cache.delete(f'submenu-{submenu_id}')
    return data


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}',
    response_model=Submenu,
    status_code=200,
)
async def patch_submenu(
    submenu_id: UUID,
    update_data: SubmenuUpdatePatch,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> Any:
    data = await submenu_usecase.update_submenu(
        submenu_id,
        update_data.model_dump(exclude_none=True),
    )
    cache.delete('submenus')
    cache.delete(f'submenu-{submenu_id}')
    return data


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}',
    response_model=None,
    status_code=200,
)
async def delete_submenu(
    submenu_id: UUID,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
    cache: Annotated[CacheInterface, Depends()],
) -> None:
    await submenu_usecase.delete_submenu(submenu_id)
    cache.clear()
