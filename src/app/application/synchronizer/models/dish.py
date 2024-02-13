from dataclasses import dataclass
from decimal import Decimal
from typing import Literal
from uuid import UUID


@dataclass
class Dish:
    id: UUID
    title: str
    description: str
    price: Decimal
    submenu_id: UUID

    status: Literal['to_insert', 'to_update', 'no_modified'] = 'no_modified'
