from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, ConfigDict

from app.application.models.dish import Dish
from app.application.models.submenu import Submenu


class BaseMenu:
    id: UUID
    title: str
    description: str


class SubmenuWithDishes(Submenu):
    dishes: list[Dish]


class SubmenuWithDishCount(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    dishes_count: int


class Menu(BaseMenu, BaseModel):
    model_config = ConfigDict(from_attributes=True)
    submenus: list[SubmenuWithDishCount]


class MenuWithoutSubmenus(BaseMenu, BaseModel):
    model_config = ConfigDict(from_attributes=True)
    submenus_count: int
    dishes_count: int


class MenuWithAllData(BaseMenu, BaseModel):
    model_config = ConfigDict(from_attributes=True)
    submenus: list[SubmenuWithDishes]


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuUpdatePut(BaseModel):
    title: str = Body(...)
    description: str = Body(...)


class MenuUpdatePatch(BaseModel):
    title: str = Body(None)
    description: str = Body(None)
