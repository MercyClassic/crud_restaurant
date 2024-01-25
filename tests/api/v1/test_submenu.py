from uuid import UUID

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.sql.functions import count

from app.infrastructure.database.models import Submenu
from tests.conftest import test_async_session_maker as async_session_maker


async def get_submenu_count():
    async with async_session_maker() as session:
        result = await session.execute(
            select(count(Submenu.id)),
        )
    return result.scalar()


async def get_submenu_from_db(
    submenu_id: UUID,
):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Submenu).where(Submenu.id == submenu_id),
        )
    result = result.scalar()
    result = {
        'id': str(result.id),
        'title': result.title,
        'description': result.description,
        'menu_id': str(result.menu_id),
    }
    return result


async def test_get_empty_submenu_list(
    client: AsyncClient,
    menu: UUID,
):
    response = await client.get(
        f'/api/v1/menus/{menu}/submenus',
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_get_submenu_list(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
    dish: UUID,
):
    menu_id, submenu_id = submenu
    response = await client.get(
        f'/api/v1/menus/{menu_id}/submenus',
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == [
        {
            'id': submenu_id,
            'title': 'Submenu 1',
            'description': 'Desc 1',
            'menu_id': menu_id,
            'dishes_count': 1,
        },
    ]


async def test_get_submenu_detail(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
    dish: UUID,
):
    menu_id, submenu_id = submenu
    response = await client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {
        'id': submenu_id,
        'title': 'Submenu 1',
        'description': 'Desc 1',
        'menu_id': menu_id,
        'dishes_count': 1,
    }


async def test_create_submenu(
    client: AsyncClient,
    menu: UUID,
):
    response = await client.post(
        f'/api/v1/menus/{menu}/submenus',
        json={
            'title': 'Submenu 1',
            'description': 'desc 1',
        },
    )
    response_data = response.json()
    expected_data = {
        'id': response_data['id'],
        'title': 'Submenu 1',
        'description': 'desc 1',
        'menu_id': menu,
    }

    assert response.status_code == 201
    assert response_data == expected_data
    assert await get_submenu_from_db(response_data['id']) == expected_data


async def test_update_submenu(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
):
    menu_id, submenu_id = submenu
    response = await client.patch(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
        json={
            'title': 'Edited Submenu 1',
            'description': 'Edited Desc 1',
        },
    )
    response_data = response.json()
    expected_data = {
        'id': submenu_id,
        'title': 'Edited Submenu 1',
        'description': 'Edited Desc 1',
        'menu_id': menu_id,
    }
    assert response.status_code == 200
    assert response_data == expected_data
    assert await get_submenu_from_db(submenu_id) == expected_data


async def test_delete_submenu(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
    dish: UUID,
):
    menu_id, submenu_id = submenu
    response = await client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    )
    assert response.status_code == 200
    assert await get_submenu_count() == 0
