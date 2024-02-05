from uuid import UUID

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import undefer
from sqlalchemy.sql.functions import count

from app.infrastructure.database.models import Menu
from tests.conftest import reverse
from tests.conftest import test_async_session_maker as async_session_maker


async def get_menu_count() -> int:
    async with async_session_maker() as session:
        result = await session.execute(
            select(count(Menu.id)),
        )
    return result.scalar()


async def get_menu_from_db(
    menu_id: UUID,
) -> dict[str, str]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Menu)
            .where(Menu.id == menu_id)
            .options(
                undefer(Menu.submenus_count),
                undefer(Menu.dishes_count),
            ),
        )
    result = result.scalar()
    result = {
        'id': str(result.id),
        'title': result.title,
        'description': result.description,
        'submenus_count': result.submenus_count,
        'dishes_count': result.dishes_count,
    }
    return result


async def test_get_empty_menu_list(
    client: AsyncClient,
) -> None:
    url = reverse('get_menus')
    response = await client.get(url)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_menu_list(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
    dish: UUID,
) -> None:
    menu_id, submenu_id = submenu
    url = reverse('get_menus')
    response = await client.get(url)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == [
        {
            'id': menu_id,
            'title': 'Menu 1',
            'description': 'Desc 1',
            'submenus': [
                {
                    'id': submenu_id,
                    'dishes_count': 1,
                },
            ],
        },
    ]


async def test_get_menu_detail(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
    dish: UUID,
) -> None:
    menu_id, submenu_id = submenu
    url = reverse('get_menu', menu_id=menu_id)
    response = await client.get(url)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {
        'id': menu_id,
        'title': 'Menu 1',
        'description': 'Desc 1',
        'submenus_count': 1,
        'dishes_count': 1,
    }


async def test_create_menu(
    client: AsyncClient,
) -> None:
    url = reverse('get_menus')
    response = await client.post(
        url,
        json={
            'title': 'Menu 1',
            'description': 'desc 1',
        },
    )
    response_data = response.json()
    expected_data = {
        'id': response_data['id'],
        'title': 'Menu 1',
        'description': 'desc 1',
        'submenus_count': 0,
        'dishes_count': 0,
    }

    assert response.status_code == 201
    assert response_data == expected_data
    assert await get_menu_from_db(response_data['id']) == expected_data


async def test_update_menu(
    client: AsyncClient,
    menu: UUID,
) -> None:
    url = reverse('patch_menu', menu_id=menu)
    response = await client.patch(
        url,
        json={
            'title': 'Edited Menu 1',
            'description': 'Edited Desc 1',
        },
    )
    response_data = response.json()
    expected_data = {
        'id': menu,
        'title': 'Edited Menu 1',
        'description': 'Edited Desc 1',
        'submenus_count': 0,
        'dishes_count': 0,
    }
    assert response.status_code == 200
    assert response_data == expected_data
    assert await get_menu_from_db(menu) == expected_data


async def test_delete_menu(
    client: AsyncClient,
    menu: UUID,
) -> None:
    url = reverse('patch_menu', menu_id=menu)
    response = await client.delete(url)
    assert response.status_code == 200
    assert await get_menu_count() == 0
