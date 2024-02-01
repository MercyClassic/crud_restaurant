from typing import AsyncGenerator

import pytest
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import Dish, Menu, Submenu


@pytest.fixture
async def menu(
    test_session: AsyncSession,
) -> AsyncGenerator[str, None]:
    """MENU FOR SUBMENU/DISH TESTS"""
    menu = await test_session.execute(
        insert(Menu)
        .values(
            title='Menu 1',
            description='Desc 1',
        )
        .returning(Menu),
    )
    menu = menu.scalar()
    await test_session.commit()

    yield str(menu.id)

    await test_session.execute(
        delete(Menu).where(Menu.id == menu.id),
    )
    await test_session.commit()


@pytest.fixture
async def submenu(
    menu: str,
    test_session: AsyncSession,
) -> AsyncGenerator[tuple[str, str], None]:
    """SUBMENU FOR DISH TESTS, RETURNING menu_uuid and submenu_uuid"""
    submenu = await test_session.execute(
        insert(Submenu)
        .values(
            title='Submenu 1',
            description='Desc 1',
            menu_id=menu,
        )
        .returning(Submenu),
    )
    submenu = submenu.scalar()
    await test_session.commit()

    yield menu, str(submenu.id)

    await test_session.execute(
        delete(Submenu).where(Submenu.id == submenu.id),
    )
    await test_session.commit()


@pytest.fixture
async def dish(
    submenu: tuple[str, str],
    test_session: AsyncSession,
) -> AsyncGenerator[str, None]:
    """DISH FOR DISH TESTS"""
    dish = await test_session.execute(
        insert(Dish)
        .values(
            title='Dish 1',
            description='Desc 1',
            price=123.123,
            submenu_id=submenu[1],
        )
        .returning(Dish),
    )
    dish = dish.scalar()
    await test_session.commit()

    yield str(dish.id)

    await test_session.execute(
        delete(Dish).where(Dish.id == dish.id),
    )
    await test_session.commit()
