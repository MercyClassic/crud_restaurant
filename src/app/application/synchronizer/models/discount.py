from typing import NamedTuple
from uuid import UUID


class Discount(NamedTuple):
    dish_id: UUID
    value: int
