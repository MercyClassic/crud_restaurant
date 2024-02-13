from dataclasses import dataclass
from typing import Literal
from uuid import UUID


@dataclass
class Submenu:
    id: UUID
    title: str
    description: str
    menu_id: UUID

    status: Literal['to_insert', 'to_update', 'no_modified'] = 'to_insert'
