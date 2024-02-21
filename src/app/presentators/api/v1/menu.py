from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks

from app.application.models.menu import (
    Menu,
    MenuCreate,
    MenuUpdatePatch,
    MenuUpdatePut,
    MenuWithAllData,
    MenuWithoutSubmenus,
)
from app.domain.interfaces.services.menu import MenuServiceInterface
from app.infrastructure.cache.interfaces.menu import MenuCacheServiceInterface

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
    '/menus_all_data',
    tags=['GET'],
    response_model=list[MenuWithAllData],
    status_code=200,
)
async def menus_with_all_data(
    menu_usecase: Annotated[MenuServiceInterface, Depends()],
):
    data = await menu_usecase.get_menus_with_all_data()
    return data


@router.get(
    '/menus',
    tags=['GET'],
    response_model=list[Menu],
    status_code=200,
)
async def get_menus(
    menu_usecase: Annotated[MenuServiceInterface, Depends()],
) -> Any:
    data = await menu_usecase.get_menus()
    return data


@router.post(
    '/menus',
    tags=['POST'],
    response_model=MenuWithoutSubmenus,
    status_code=201,
)
async def create_menu(
    menu_data: MenuCreate,
    menu_usecase: Annotated[MenuServiceInterface, Depends()],
    menu_cache_service: Annotated[MenuCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> Any:
    data = await menu_usecase.create_menu(
        title=menu_data.title,
        description=menu_data.description,
    )
    background_tasks.add_task(
        menu_cache_service.invalidate_cache_after_create_menu,
    )
    return data


@router.get(
    '/menus/{menu_id}',
    tags=['GET'],
    response_model=MenuWithoutSubmenus,
    status_code=200,
)
async def get_menu(
    menu_id: UUID,
    menu_usecase: Annotated[MenuServiceInterface, Depends()],
) -> Any:
    data = await menu_usecase.get_menu(menu_id)
    return data


@router.put(
    '/menus/{menu_id}',
    tags=['PUT'],
    response_model=MenuWithoutSubmenus,
    status_code=200,
)
async def put_menu(
    menu_id: UUID,
    update_data: MenuUpdatePut,
    menu_usecase: Annotated[MenuServiceInterface, Depends()],
    menu_cache_service: Annotated[MenuCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> Any:
    data = await menu_usecase.update_menu(
        menu_id=menu_id,
        title=update_data.title,
        description=update_data.description,
    )
    background_tasks.add_task(
        menu_cache_service.invalidate_cache_after_update_menu,
        menu_id,
    )
    return data


@router.patch(
    '/menus/{menu_id}',
    tags=['PATCH'],
    response_model=MenuWithoutSubmenus,
    status_code=200,
)
async def patch_menu(
    menu_id: UUID,
    update_data: MenuUpdatePatch,
    menu_usecase: Annotated[MenuServiceInterface, Depends()],
    menu_cache_service: Annotated[MenuCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> Any:
    data = await menu_usecase.update_menu(
        menu_id=menu_id,
        title=update_data.title,
        description=update_data.description,
    )
    background_tasks.add_task(
        menu_cache_service.invalidate_cache_after_update_menu,
        menu_id,
    )
    return data


@router.delete(
    '/menus/{menu_id}',
    tags=['DELETE'],
    response_model=None,
    status_code=200,
)
async def delete_menu(
    menu_id: UUID,
    menu_usecase: Annotated[MenuServiceInterface, Depends()],
    menu_cache_service: Annotated[MenuCacheServiceInterface, Depends()],
    background_tasks: BackgroundTasks,
) -> None:
    await menu_usecase.delete_menu(menu_id)
    background_tasks.add_task(
        menu_cache_service.invalidate_cache_after_delete_menu,
        menu_id,
    )
