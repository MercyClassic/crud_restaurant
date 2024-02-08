from typing import NamedTuple
from uuid import UUID


class Submenu(NamedTuple):
    id: UUID
    title: str
    description: str
    menu_id: UUID
