import json
from typing import Sequence
from uuid import UUID

from app.application.encoders.json import JSONEncoder
from app.domain.exceptions.submenu import SubmenuNotFound
from app.infrastructure.cache.interfaces.submenu import SubmenuCacheServiceInterface
from app.infrastructure.database.interfaces.uow.uow import UoWInterface
from app.infrastructure.database.models import Submenu


class SubmenuService:
    def __init__(
        self,
        uow: UoWInterface,
        cache: SubmenuCacheServiceInterface,
    ):
        self._uow = uow
        self._cache = cache

    async def get_submenus(self) -> Sequence[Submenu]:
        submenus = self._cache.get_submenus()
        if not submenus:
            submenus = await self._uow.submenu_repo.get_submenus()
            encoder = JSONEncoder(submenus)
            submenus = encoder.data
            self._cache.set_submenus(json.dumps(submenus))
        else:
            submenus = json.loads(submenus)
        return submenus

    async def get_submenu(
        self,
        submenu_id: UUID,
        menu_id: UUID,
    ) -> Submenu:
        submenu = self._cache.get_submenu(submenu_id, menu_id)
        if not submenu:
            submenu = await self._uow.submenu_repo.get_submenu(submenu_id)
            if not submenu:
                raise SubmenuNotFound
            encoder = JSONEncoder(submenu)
            submenu = encoder.data
            self._cache.set_submenu(submenu_id, menu_id, json.dumps(submenu))
        else:
            submenu = json.loads(submenu)
        return submenu

    async def create_submenu(
        self,
        menu_id: UUID,
        title: str,
        description: str,
    ) -> Submenu:
        submenu = await self._uow.submenu_repo.save_submenu(
            menu_id=menu_id,
            title=title,
            description=description,
        )
        await self._uow.commit()
        submenu = await self._uow.submenu_repo.get_submenu(submenu.id)
        return submenu

    async def update_submenu(
        self,
        submenu_id: UUID,
        title: str | None,
        description: str | None,
    ) -> Submenu:
        submenu = await self._uow.submenu_repo.update_submenu(
            submenu_id=submenu_id,
            title=title,
            description=description,
        )
        await self._uow.commit()
        submenu = await self._uow.submenu_repo.get_submenu(submenu.id)
        return submenu

    async def delete_submenu(
        self,
        submenu_id: UUID,
    ) -> None:
        await self._uow.submenu_repo.delete_submenu(submenu_id)
        await self._uow.commit()
