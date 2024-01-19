from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter
from starlette import status
from starlette.responses import JSONResponse

from app.application.models.menu import (
    Menu,
    MenuCreate,
    MenuUpdatePatch,
    MenuUpdatePut,
    MenuWithoutSubmenus,
)
from app.domain.interfaces.usecases.menu import MenuUsecaseInterface

router = APIRouter()


@router.get('/menus')
async def get_menus(
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
):
    data = await menu_usecase.get_menus()
    data = TypeAdapter(List[Menu]).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.post('/menus')
async def create_menu(
    menu_data: MenuCreate,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
):
    data = await menu_usecase.create_menu(menu_data.model_dump())
    data = TypeAdapter(MenuWithoutSubmenus).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(data),
    )


@router.get('/menus/{menu_id}')
async def get_menu(
    menu_id: UUID,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
):
    data = await menu_usecase.get_menu(menu_id)
    data = TypeAdapter(MenuWithoutSubmenus).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.put('/menus/{menu_id}')
async def put_menu(
    menu_id: UUID,
    update_data: MenuUpdatePut,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
):
    data = await menu_usecase.update_menu(menu_id, update_data.model_dump(exclude_none=True))
    data = TypeAdapter(MenuWithoutSubmenus).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.patch('/menus/{menu_id}')
async def patch_menu(
    menu_id: UUID,
    update_data: MenuUpdatePatch,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
):
    data = await menu_usecase.update_menu(menu_id, update_data.model_dump(exclude_none=True))
    data = TypeAdapter(MenuWithoutSubmenus).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.delete('/menus/{menu_id}')
async def delete_menu(
    menu_id: UUID,
    menu_usecase: Annotated[MenuUsecaseInterface, Depends()],
):
    await menu_usecase.delete_menu(menu_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=None,
    )
