from typing import List, TYPE_CHECKING
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


from app.database import db
from .plant_family_category import plant_family_category
from .utils import ModelMixin, generate_uuid

if TYPE_CHECKING:
    from .plant_family import PlantFamily


class PlantCategory(db.Model, ModelMixin):
    __tablename__ = "plant_categories"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Fields
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
    svg_icon: orm.Mapped[str] = orm.mapped_column(sa.Text)

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)

    plant_families: orm.Mapped[List["PlantFamily"]] = orm.relationship(
        secondary=plant_family_category,
        back_populates="categories",
    )

    def __repr__(self):
        return f"<Id: {self.id}, PlantFamily: {self.name}>"
