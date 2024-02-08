from typing import NamedTuple
from uuid import UUID


class Menu(NamedTuple):
    id: UUID
    title: str
    description: str
