from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models import Base


class Dish(Base):
    __tablename__ = 'dish'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )
    submenu_id: Mapped[int] = mapped_column(
        ForeignKey(
            'submenu.id',
            ondelete='CASCADE',
        ),
    )
