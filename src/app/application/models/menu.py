from typing import List
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, ConfigDict, Field


class SubmenuWithDishCount(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    dish_count: int = Field(serialization_alias='dishes_count')


class Menu(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    submenus: List[SubmenuWithDishCount]


class MenuWithoutSubmenus(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuUpdatePut(BaseModel):
    title: str = Body(...)
    description: str = Body(...)


class MenuUpdatePatch(BaseModel):
    title: str = Body(None)
    description: str = Body(None)
