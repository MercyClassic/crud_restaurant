from decimal import Decimal
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, ConfigDict


class Dish(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    price: Decimal
    submenu_id: UUID


class DishCreate(BaseModel):
    title: str
    description: str
    price: Decimal


class DishUpdatePatch(BaseModel):
    title: str = Body(None)
    description: str = Body(None)
    price: Decimal = Body(None)
    submenu_id: UUID = Body(None)


class DishUpdatePut(BaseModel):
    title: str = Body(...)
    description: str = Body(...)
    price: Decimal = Body(...)
    submenu_id: UUID = Body(...)
