from uuid import UUID

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.sql.functions import count

from app.infrastructure.database.models import Dish
from tests.conftest import reverse
from tests.conftest import test_async_session_maker as async_session_maker


async def get_dish_count() -> Dish:
    async with async_session_maker() as session:
        result = await session.execute(
            select(count(Dish.id)),
        )
    return result.scalar()


async def get_dish_from_db(
    dish_id: UUID,
) -> dict:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Dish).where(Dish.id == dish_id),
        )
    result = result.scalar()
    result = {
        'id': str(result.id),
        'title': result.title,
        'description': result.description,
        'submenu_id': str(result.submenu_id),
        'price': str(result.price),
    }
    return result


async def test_get_empty_dish_list(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
) -> None:
    menu_id, submenu_id = submenu
    path_params = {
        'menu_id': menu_id,
        'submenu_id': submenu_id,
    }
    url = reverse('get_dishes', **path_params)
    response = await client.get(url)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_dish_list(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
    dish: UUID,
) -> None:
    menu_id, submenu_id = submenu
    path_params = {
        'menu_id': menu_id,
        'submenu_id': submenu_id,
    }
    url = reverse('get_dishes', **path_params)
    response = await client.get(url)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == [
        {
            'id': dish,
            'title': 'Dish 1',
            'description': 'Desc 1',
            'price': '123.12',
            'submenu_id': submenu_id,
        },
    ]


async def test_get_dish_detail(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
    dish: UUID,
) -> None:
    menu_id, submenu_id = submenu
    path_params = {
        'menu_id': menu_id,
        'submenu_id': submenu_id,
        'dish_id': dish,
    }
    url = reverse('get_dish', **path_params)
    response = await client.get(url)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {
        'id': dish,
        'title': 'Dish 1',
        'description': 'Desc 1',
        'price': '123.12',
        'submenu_id': submenu_id,
    }


async def test_create_dish(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
) -> None:
    menu_id, submenu_id = submenu
    path_params = {
        'menu_id': menu_id,
        'submenu_id': submenu_id,
    }
    url = reverse('create_dish', **path_params)
    response = await client.post(
        url,
        json={
            'title': 'dish 1',
            'description': 'desc 1',
            'price': 123.123,
        },
    )
    response_data = response.json()
    expected_data = {
        'id': response_data['id'],
        'title': 'dish 1',
        'description': 'desc 1',
        'price': '123.12',
        'submenu_id': submenu_id,
    }

    assert response.status_code == 201
    assert response_data == expected_data
    assert await get_dish_from_db(response_data['id']) == expected_data


async def test_update_dish(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
    dish: UUID,
) -> None:
    menu_id, submenu_id = submenu
    path_params = {
        'menu_id': menu_id,
        'submenu_id': submenu_id,
        'dish_id': dish,
    }
    url = reverse('patch_dish', **path_params)
    response = await client.patch(
        url,
        json={
            'title': 'Edited Dish 1',
            'description': 'Edited Desc 1',
            'price': '456.45',
        },
    )
    response_data = response.json()
    expected_data = {
        'id': dish,
        'title': 'Edited Dish 1',
        'description': 'Edited Desc 1',
        'price': '456.45',
        'submenu_id': submenu_id,
    }
    assert response.status_code == 200
    assert response_data == expected_data
    assert await get_dish_from_db(dish) == expected_data


async def test_delete_dish(
    client: AsyncClient,
    submenu: tuple[UUID, UUID],
    dish: UUID,
) -> None:
    menu_id, submenu_id = submenu
    path_params = {
        'menu_id': menu_id,
        'submenu_id': submenu_id,
        'dish_id': dish,
    }
    url = reverse('delete_dish', **path_params)
    response = await client.delete(url)
    assert response.status_code == 200
    assert await get_dish_count() == 0
