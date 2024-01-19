from typing import List  # , TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship
from sqlalchemy.sql.functions import count

from app.infrastructure.database.models import Base

# if TYPE_CHECKING:
from app.infrastructure.database.models.dish import Dish


class Submenu(Base):
    __tablename__ = 'submenu'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    description: Mapped[str]
    menu_id: Mapped[int] = mapped_column(ForeignKey('menu.id'))

    dishes: Mapped[List['Dish']] = relationship(backref='submenu')

    dish_count: Mapped[int] = column_property(
        select(count(Dish.id)).where(Dish.submenu_id == id).scalar_subquery(),
        deferred=True,
    )
