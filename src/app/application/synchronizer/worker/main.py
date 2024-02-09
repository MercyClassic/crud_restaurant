import os
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import numpy as np
import pandas as pd
from asgiref.sync import async_to_sync
from celery import Celery
from redis import Redis

from app.application.synchronizer.interfaces.repositories.sync import (
    SyncRepositoryInterface,
)
from app.application.synchronizer.models import Discount, Dish, Menu, Submenu
from app.application.synchronizer.repositories.sync import SyncRepository
from app.infrastructure.cache.interfaces.base import CacheServiceInterface
from app.infrastructure.cache.services.redis.base import BaseRedisCacheService
from app.infrastructure.database.database import create_async_session_maker


class SynchronizerDB:
    def __init__(
        self,
        sync_repo: SyncRepositoryInterface,
        cache: CacheServiceInterface,
    ):
        self._menus: list[Menu] = []
        self._submenus: list[Submenu] = []
        self._dishes: list[Dish] = []
        self._discounts: list[Discount] = []
        self._sync_repo = sync_repo
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

    async def parse_data_to_sync_db(self) -> None:
        table_path = f'{Path(__file__).parent.parent}/admin/Menu.xlsx'
        df = pd.read_excel(table_path, header=None)
        df.replace(np.nan, None, inplace=True)

        menu_id: UUID = None  # type: ignore[assignment]
        submenu_id: UUID = None  # type: ignore[assignment]
        for row in df.values:
            if all([value is None for value in row[3:]]):
                """Если все элементы после 3 являются None, то этот элемент - меню"""
                menu_id = row[0].strip()
                title = row[1].strip()
                description = row[2].strip()
                self.add_menu(
                    entity_id=menu_id,
                    title=title,
                    description=description,
                )
            elif all([value is None for value in row[4:]]):
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
            elif all([value is None for value in row[:2]]):
                """Если первые два элемента являются None, то этот элемент - блюдо"""
                dish_id = row[2].strip()
                title = row[3].strip()
                description = row[4].strip()
                price = Decimal(row[5])
                discount_value = row[6]
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
        await self.parse_data_to_sync_db()

        self._cache.delete_by_pattern('*')
        await self._sync_repo.clear_db()

        await self._sync_repo.bulk_insert_menus(self._menus)
        await self._sync_repo.bulk_insert_submenus(self._submenus)
        await self._sync_repo.bulk_insert_dishes(self._dishes)
        await self._sync_repo.commit()

        for discount in self._discounts:
            self._cache.set(f'discount_for_{discount.dish_id}', discount.value, ex=15)


def create_celery_worker() -> Celery:
    worker = Celery(
        'synchronizer',
        broker=f'amqp://{os.environ["RABBITMQ_HOST"]}:5672',
    )
    return worker


worker = create_celery_worker()


@worker.task
def synchronize_db() -> None:
    async_session_maker = create_async_session_maker(os.environ['db_uri'])
    async_session = async_session_maker()
    sync_repo = SyncRepository(async_session)

    cache = BaseRedisCacheService(
        Redis(
            os.environ['REDIS_HOST'],
            decode_responses=True,
        ),
    )

    synchronizer = SynchronizerDB(sync_repo, cache)
    async_to_sync(synchronizer.run)()
    async_to_sync(async_session.close)()


worker.add_periodic_task(15, synchronize_db)
