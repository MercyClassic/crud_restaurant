from decimal import Decimal
from pathlib import Path
from typing import Iterable
from uuid import UUID

import gspread

from app.application.synchronizer.interfaces.uow import SynchronizerUowInterface
from app.application.synchronizer.models import Discount, Dish, Menu, Submenu
from app.infrastructure.cache.interfaces.base import CacheServiceInterface


class SynchronizerDB:
    def __init__(
        self,
        sync_uow: SynchronizerUowInterface,
        cache: CacheServiceInterface,
    ):
        self._menus: list[Menu] = []
        self._submenus: list[Submenu] = []
        self._dishes: list[Dish] = []
        self._discounts: list[Discount] = []

        self._sync_uow = sync_uow
        self._cache = cache

    def add_menu(
        self,
        entity_id: UUID,
        title: str,
        description: str,
    ) -> None:
        self._menus.append(
            Menu(
                id=entity_id,
                title=title,
                description=description,
            ),
        )

    def add_submenu(
        self,
        entity_id: UUID,
        title: str,
        description: str,
        menu_id: UUID,
    ) -> None:
        self._submenus.append(
            Submenu(
                id=entity_id,
                title=title,
                description=description,
                menu_id=menu_id,
            ),
        )

    def add_dish(
        self,
        entity_id: UUID,
        title: str,
        description: str,
        price: Decimal,
        submenu_id: UUID,
    ) -> None:
        self._dishes.append(
            Dish(
                id=entity_id,
                title=title,
                description=description,
                price=price,
                submenu_id=submenu_id,
            ),
        )

    def add_discount(
        self,
        entity_id: UUID,
        value: int,
    ) -> None:
        self._discounts.append(
            Discount(
                dish_id=entity_id,
                value=value,
            ),
        )

    def _prepare_db_data(
        self,
        db_menus: Iterable[Menu],
        db_submenus: Iterable[Submenu],
        db_dishes: Iterable[Dish],
    ) -> tuple[dict, dict, dict]:
        menus = {
            str(menu.id): {
                'entity': menu,
                'is_checked': False,
            }
            for menu in db_menus
        }
        submenus = {
            str(submenu.id): {
                'entity': submenu,
                'is_checked': False,
            }
            for submenu in db_submenus
        }
        dishes = {
            str(dish.id): {
                'entity': dish,
                'is_checked': False,
            }
            for dish in db_dishes
        }
        return menus, submenus, dishes

    def _compare_menus(self, db_menus: dict[str, dict]) -> None:
        for menu in self._menus:
            db_menu = db_menus.get(str(menu.id))
            if db_menu:
                entity = db_menu['entity']
                if entity.title != menu.title or entity.description != menu.description:
                    menu.status = 'to_update'
                else:
                    menu.status = 'no_modified'
                db_menu['is_checked'] = True

    def _compare_submenus(self, db_menus: dict[str, dict]) -> None:
        for submenu in self._submenus:
            db_submenu = db_menus.get(str(submenu.id))
            if db_submenu:
                entity = db_submenu['entity']
                if entity.title != submenu.title or entity.description != submenu.description:
                    submenu.status = 'to_update'
                else:
                    submenu.status = 'no_modified'
                db_submenu['is_checked'] = True

    def _compare_dishes(self, db_menus: dict[str, dict]) -> None:
        for dish in self._dishes:
            db_dish = db_menus.get(str(dish.id))
            if db_dish:
                entity = db_dish['entity']
                if entity.title != dish.title or entity.description != dish.description or entity.price != dish.price:
                    dish.status = 'to_update'
                else:
                    dish.status = 'no_modified'
                db_dish['is_checked'] = True

    async def _process_delete(
        self,
        db_menus: dict[str, dict],
        db_submenus: dict[str, dict],
        db_dishes: dict[str, dict],
    ) -> None:
        menus_to_delete = [d['entity'].id for d in db_menus.values() if d['is_checked'] is False]
        if menus_to_delete:
            await self._sync_uow.menu_repo.bulk_delete_menus(menus_to_delete)
        submenus_to_delete = [
            d['entity'].id for d in db_submenus.values() if d['is_checked'] is False
        ]
        if submenus_to_delete:
            await self._sync_uow.submenu_repo.bulk_delete_submenus(submenus_to_delete)
        dishes_to_delete = [d['entity'].id for d in db_dishes.values() if d['is_checked'] is False]
        if dishes_to_delete:
            await self._sync_uow.dish_repo.bulk_delete_dishes(dishes_to_delete)

    async def _process_update(self) -> None:
        menus_to_update = [menu for menu in self._menus if menu.status == 'to_update']
        if menus_to_update:
            for menu in menus_to_update:
                await self._sync_uow.menu_repo.update_menu(menu)
        submenus_to_update = [
            submenu for submenu in self._submenus if submenu.status == 'to_update'
        ]
        if submenus_to_update:
            for submenu in submenus_to_update:
                await self._sync_uow.submenu_repo.update_submenu(submenu)
        dishes_to_update = [dish for dish in self._dishes if dish.status == 'to_update']
        if dishes_to_update:
            for dish in dishes_to_update:
                await self._sync_uow.dish_repo.update_dish(dish)

    async def _process_insert(self) -> None:
        menus_to_insert = [menu for menu in self._menus if menu.status == 'to_insert']
        if menus_to_insert:
            await self._sync_uow.menu_repo.bulk_insert_menus(menus_to_insert)
        submenus_to_insert = [
            submenu for submenu in self._submenus if submenu.status == 'to_insert'
        ]
        if submenus_to_insert:
            await self._sync_uow.submenu_repo.bulk_insert_submenus(submenus_to_insert)
        dishes_to_insert = [dish for dish in self._dishes if dish.status == 'to_insert']
        if dishes_to_insert:
            await self._sync_uow.dish_repo.bulk_insert_dishes(dishes_to_insert)

    def _set_discount_in_cache(self) -> None:
        for discount in self._discounts:
            self._cache.set(f'discount_for_{discount.dish_id}', discount.value, ex=15)

    def parse_data_to_sync_db(self) -> None:
        gs = gspread.service_account(filename=f'{Path(__file__).parent}/credentials.json')
        sh = gs.open('Menu')

        menu_id: UUID = None  # type: ignore[assignment]
        submenu_id: UUID = None  # type: ignore[assignment]
        for row in sh.sheet1.get_values():
            if all([value == '' for value in row[3:]]):
                """Если все элементы после 3 являются None, то этот элемент - меню"""
                menu_id = row[0].strip()
                title = row[1].strip()
                description = row[2].strip()
                self.add_menu(
                    entity_id=menu_id,
                    title=title,
                    description=description,
                )
            elif all([value == '' for value in row[4:]]):
                """Если все элементы после 4 являются None, то этот элемент - подменю"""
                submenu_id = row[1].strip()
                title = row[2].strip()
                description = row[3].strip()
                self.add_submenu(
                    entity_id=submenu_id,
                    title=title,
                    description=description,
                    menu_id=menu_id,
                )
            elif all([value == '' for value in row[:2]]):
                """Если первые два элемента являются None, то этот элемент - блюдо"""
                dish_id = row[2].strip()
                title = row[3].strip()
                description = row[4].strip()
                price = Decimal(row[5].replace(',', '.'))
                discount_value = row[6].replace(',', '.')
                self.add_dish(
                    entity_id=dish_id,
                    title=title,
                    description=description,
                    price=price,
                    submenu_id=submenu_id,
                )
                self.add_discount(
                    entity_id=dish_id,
                    value=discount_value,
                )

    async def run(self) -> None:
        self.parse_data_to_sync_db()

        db_menus = await self._sync_uow.menu_repo.get_menus()
        db_submenus = await self._sync_uow.submenu_repo.get_submenus()
        db_dishes = await self._sync_uow.dish_repo.get_dishes()
        db_menus, db_submenus, db_dishes = self._prepare_db_data(db_menus, db_submenus, db_dishes)

        self._compare_menus(db_menus)
        self._compare_submenus(db_submenus)
        self._compare_dishes(db_dishes)

        await self._process_delete(db_menus, db_submenus, db_dishes)
        await self._process_update()
        await self._process_insert()

        await self._sync_uow.commit()

        self._cache.delete_by_pattern('*')

        self._set_discount_in_cache()
