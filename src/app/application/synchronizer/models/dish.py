from decimal import Decimal
from typing import NamedTuple
from uuid import UUID


class Dish(NamedTuple):
    id: UUID
    title: str
    description: str
    price: Decimal
    submenu_id: UUID
