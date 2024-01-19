from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship
from sqlalchemy.sql.functions import count

from app.infrastructure.database.models import Base
from app.infrastructure.database.models.dish import Dish

# if TYPE_CHECKING:
from app.infrastructure.database.models.submenu import Submenu


class Menu(Base):
    __tablename__ = 'menu'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    description: Mapped[str]

    submenus_count: Mapped[int] = column_property(
        select(count(Submenu.id)).where(Submenu.menu_id == id).scalar_subquery(),
        deferred=True,
    )
    dishes_count: Mapped[int] = column_property(
        select(count(Dish.id)).join(Submenu).where(Submenu.menu_id == id).scalar_subquery(),
        deferred=True,
    )

    submenus: Mapped[List['Submenu']] = relationship(backref='menu')
