from typing import TYPE_CHECKING, List
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


from app.database import db
from .utils import ModelMixin, generate_uuid

from .plant_variety_illness import plant_variety_illness
from .plant_variety_pest import plant_variety_pest
from .plant_variety_photo import plant_variety_photo

if TYPE_CHECKING:
    from .photo import Photo
    from .illness import Illness
    from .pest import Pest
    from .condition import Condition
    from .plant_family import PlantFamily


class PlantVariety(db.Model, ModelMixin):
    __tablename__ = "plant_varieties"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    plant_family_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("plant_families.id"), nullable=False
    )

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )

    features: orm.Mapped[str] = orm.mapped_column(
        sa.String(1024), default="", nullable=True
    )
    condition: orm.Mapped["Condition"] = orm.relationship(uselist=False)

    illnesses: orm.Mapped[List["Illness"]] = orm.relationship(
        secondary=plant_variety_illness, back_populates="plant_varieties"
    )
    pests: orm.Mapped[List["Pest"]] = orm.relationship(
        secondary=plant_variety_pest, back_populates="plant_varieties"
    )
    family: orm.Mapped[List["PlantFamily"]] = orm.relationship(
        back_populates="plant_varieties"
    )
    photos: orm.Mapped[List["Photo"]] = orm.relationship(secondary=plant_variety_photo)

    def __repr__(self):
        return f"<Id: {self.id}, PlantVariety: {self.name}>"
