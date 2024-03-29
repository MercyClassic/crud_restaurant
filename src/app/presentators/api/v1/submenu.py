from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks

from app.application.models.submenu import (
    Submenu,
    SubmenuCreate,
    SubmenuUpdatePatch,
    SubmenuUpdatePut,
    SubmenuWithDishCount,
)
from app.domain.interfaces.services.submenu import SubmenuServiceInterface
from app.infrastructure.cache.interfaces.submenu import SubmenuCacheServiceInterface

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
    tags=['GET'],
    response_model=list[SubmenuWithDishCount],
    status_code=200,
)
async def get_submenus(
    submenu_usecase: Annotated[SubmenuServiceInterface, Depends()],
) -> Any:
    data = await submenu_usecase.get_submenus()
    return data


@router.post(
    '/menus/{menu_id}/submenus',
    tags=['POST'],
    response_model=Submenu,
    status_code=201,
)
async def create_submenu(
    menu_id: UUID,
    submenu_data: SubmenuCreate,
    submenu_usecase: Annotated[SubmenuServiceInterface, Depends()],
    submenu_cache_service: Annotated[SubmenuCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> Any:
    data = await submenu_usecase.create_submenu(
        menu_id=menu_id,
        title=submenu_data.title,
        description=submenu_data.description,
    )
    background_tasks.add_task(
        submenu_cache_service.invalidate_cache_after_create_submenu,
        menu_id,
    )
    return data


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}',
    tags=['GET'],
    response_model=SubmenuWithDishCount,
    status_code=200,
)
async def get_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_usecase: Annotated[SubmenuServiceInterface, Depends()],
) -> Any:
    data = await submenu_usecase.get_submenu(
        submenu_id=submenu_id,
        menu_id=menu_id,
    )
    return data


@router.put(
    '/menus/{menu_id}/submenus/{submenu_id}',
    tags=['PUT'],
    response_model=Submenu,
    status_code=200,
)
async def put_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    update_data: SubmenuUpdatePut,
    submenu_usecase: Annotated[SubmenuServiceInterface, Depends()],
    submenu_cache_service: Annotated[SubmenuCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> Any:
    data = await submenu_usecase.update_submenu(
        submenu_id=submenu_id,
        title=update_data.title,
        description=update_data.description,
    )
    background_tasks.add_task(
        submenu_cache_service.invalidate_cache_after_update_submenu,
        submenu_id,
        menu_id,
    )
    return data


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}',
    tags=['PATCH'],
    response_model=Submenu,
    status_code=200,
)
async def patch_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    update_data: SubmenuUpdatePatch,
    submenu_usecase: Annotated[SubmenuServiceInterface, Depends()],
    submenu_cache_service: Annotated[SubmenuCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> Any:
    data = await submenu_usecase.update_submenu(
        submenu_id=submenu_id,
        title=update_data.title,
        description=update_data.description,
    )
    background_tasks.add_task(
        submenu_cache_service.invalidate_cache_after_update_submenu,
        submenu_id,
        menu_id,
    )
    return data


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}',
    tags=['DELETE'],
    response_model=None,
    status_code=200,
)
async def delete_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_usecase: Annotated[SubmenuServiceInterface, Depends()],
    submenu_cache_service: Annotated[SubmenuCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> None:
    await submenu_usecase.delete_submenu(
        submenu_id=submenu_id,
    )
    background_tasks.add_task(
        submenu_cache_service.invalidate_cache_after_delete_submenu,
        submenu_id,
        menu_id,
    )
