from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, ConfigDict


class Submenu(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    menu_id: UUID


class SubmenuWithDishCount(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    menu_id: UUID
    dishes_count: int


class SubmenuCreate(BaseModel):
    title: str
    description: str


class SubmenuUpdatePut(BaseModel):
    title: str = Body(...)
    description: str = Body(...)


class SubmenuUpdatePatch(BaseModel):
    title: str = Body(None)
    description: str = Body(None)
