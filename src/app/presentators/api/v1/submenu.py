from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter
from starlette import status
from starlette.responses import JSONResponse

from app.application.models.submenu import (
    Submenu,
    SubmenuCreate,
    SubmenuUpdatePatch,
    SubmenuUpdatePut,
    SubmenuWithDishCount,
)
from app.domain.interfaces.usecases.submenu import SubmenuUsecaseInterface

router = APIRouter()


@router.get('/menus/{menu_id}/submenus')
async def get_submenus(
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
):
    data = await submenu_usecase.get_submenus()
    data = TypeAdapter(List[SubmenuWithDishCount]).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.post('/menus/{menu_id}/submenus')
async def create_submenu(
    menu_id: UUID,
    submenu_data: SubmenuCreate,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
):
    data = await submenu_usecase.create_submenu(menu_id, submenu_data.model_dump())
    data = TypeAdapter(Submenu).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(data),
    )


@router.get('/menus/{menu_id}/submenus/{submenu_id}')
async def get_submenu(
    submenu_id: UUID,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
):
    data = await submenu_usecase.get_submenu(submenu_id)
    data = TypeAdapter(SubmenuWithDishCount).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.put('/menus/{menu_id}/submenus/{submenu_id}')
async def put_submenu(
    submenu_id: UUID,
    update_data: SubmenuUpdatePut,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
):
    data = await submenu_usecase.update_submenu(
        submenu_id,
        update_data.model_dump(exclude_none=True),
    )
    data = TypeAdapter(Submenu).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.patch('/menus/{menu_id}/submenus/{submenu_id}')
async def patch_submenu(
    submenu_id: UUID,
    update_data: SubmenuUpdatePatch,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
):
    data = await submenu_usecase.update_submenu(
        submenu_id,
        update_data.model_dump(exclude_none=True),
    )
    data = TypeAdapter(Submenu).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.delete('/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(
    submenu_id: UUID,
    submenu_usecase: Annotated[SubmenuUsecaseInterface, Depends()],
):
    await submenu_usecase.delete_submenu(submenu_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=None,
    )
