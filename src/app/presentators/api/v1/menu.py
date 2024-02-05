from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.models.menu import (
    Menu,
    MenuCreate,
    MenuUpdatePatch,
    MenuUpdatePut,
    MenuWithoutSubmenus,
)
from app.domain.interfaces.usecases.menu import MenuUsecaseInterface

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
    tags=['GET'],
    response_model=list[Menu],
    status_code=200,
)
async def get_menus(
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
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
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
) -> Any:
    data = await menu_usecase.create_menu(
        title=menu_data.title,
        description=menu_data.description,
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
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
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
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
) -> Any:
    data = await menu_usecase.update_menu(
        menu_id=menu_id,
        title=update_data.title,
        description=update_data.description,
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
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
) -> Any:
    data = await menu_usecase.update_menu(
        menu_id=menu_id,
        title=update_data.title,
        description=update_data.description,
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
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
) -> None:
    await menu_usecase.delete_menu(menu_id)
