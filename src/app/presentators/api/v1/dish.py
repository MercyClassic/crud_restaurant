from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter
from starlette import status
from starlette.responses import JSONResponse

from app.application.models.dish import Dish, DishCreate, DishUpdatePatch, DishUpdatePut
from app.domain.interfaces.usecases.dish import DishUsecaseInterface

router = APIRouter()


@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes')
async def get_dishes(
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
):
    data = await dish_usecase.get_dishes()
    data = TypeAdapter(List[Dish]).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.post('/menus/{menu_id}/submenus/{submenu_id}/dishes')
async def create_dish(
    submenu_id: UUID,
    dish_data: DishCreate,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
):
    data = await dish_usecase.create_dish(submenu_id, dish_data.model_dump())
    data = TypeAdapter(Dish).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(data),
    )


@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def get_dish(
    dish_id: UUID,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
):
    data = await dish_usecase.get_dish(dish_id)
    data = TypeAdapter(Dish).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.put('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def put_dish(
    dish_id: UUID,
    update_data: DishUpdatePut,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
):
    data = await dish_usecase.update_dish(dish_id, update_data.model_dump(exclude_none=True))
    data = TypeAdapter(Dish).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.patch('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def patch_dish(
    dish_id: UUID,
    update_data: DishUpdatePatch,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
):
    data = await dish_usecase.update_dish(dish_id, update_data.model_dump(exclude_none=True))
    data = TypeAdapter(Dish).validate_python(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(data),
    )


@router.delete('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(
    dish_id: UUID,
    dish_usecase: Annotated[DishUsecaseInterface, Depends()],
):
    await dish_usecase.delete_dish(dish_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=None,
    )
