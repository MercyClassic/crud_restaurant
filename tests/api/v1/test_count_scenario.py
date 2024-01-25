from uuid import UUID

from httpx import AsyncClient
from sqlalchemy import insert

from app.infrastructure.database.models import Dish
from tests.conftest import test_async_session_maker as async_session_maker


async def create_second_dish(submenu_id: UUID) -> None:
    async with async_session_maker() as session:
        await session.execute(
            insert(Dish)
            .values(
                title='Dish 2',
                description='Desc 2',
                price=456.456,
                submenu_id=submenu_id,
            )
            .returning(Dish),
        )
        await session.commit()


async def test_count_scenario(
    client: AsyncClient,
    menu: UUID,
    submenu: tuple[UUID, UUID],
    dish: UUID,
):
    menu_id, submenu_id = submenu

    await create_second_dish(submenu_id)

    """ GET MENU DETAIL """
    response = await client.get(
        f'/api/v1/menus/{menu_id}',
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': menu_id,
        'title': 'Menu 1',
        'description': 'Desc 1',
        'submenus_count': 1,
        'dishes_count': 2,
    }

    """ GET SUBMENU DETAIL """
    response = await client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': submenu_id,
        'title': 'Submenu 1',
        'description': 'Desc 1',
        'menu_id': menu_id,
        'dishes_count': 2,
    }

    """ DELETE SUBMENU """
    response = await client.delete(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    )
    assert response.status_code == 200

    """ GET SUBMENU LIST """
    response = await client.get(
        f'/api/v1/menus/{menu_id}/submenus',
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == []

    """ GET DISH LIST """
    response = await client.get(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == []

    """ GET MENU DETAIL """
    response = await client.get(
        f'/api/v1/menus/{menu_id}',
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == {
        'id': menu_id,
        'title': 'Menu 1',
        'description': 'Desc 1',
        'submenus_count': 0,
        'dishes_count': 0,
    }

    """ DELETE MENU """
    response = await client.delete(
        f'/api/v1/menus/{menu_id}',
    )
    assert response.status_code == 200

    """ GET MENU LIST """
    response = await client.get(
        '/api/v1/menus',
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == []
