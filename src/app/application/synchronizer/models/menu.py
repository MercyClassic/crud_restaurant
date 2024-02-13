from dataclasses import dataclass
from typing import Literal
from uuid import UUID


@dataclass
class Menu:
    id: UUID
    title: str
    description: str

    status: Literal['to_insert', 'to_update', 'no_modified'] = 'no_modified'
