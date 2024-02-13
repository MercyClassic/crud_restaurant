from typing import Protocol

from app.application.synchronizer.interfaces.repositories.dish import (
    DishRepositoryInterface,
)
from app.application.synchronizer.interfaces.repositories.menu import (
    MenuRepositoryInterface,
)
from app.application.synchronizer.interfaces.repositories.submenu import (
    SubmenuRepositoryInterface,
)


class SynchronizerUowInterface(Protocol):
    menu_repo: MenuRepositoryInterface
    submenu_repo: SubmenuRepositoryInterface
    dish_repo: DishRepositoryInterface

    async def commit(self):
        raise NotImplementedError
