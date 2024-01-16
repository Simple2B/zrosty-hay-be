from typing import TYPE_CHECKING, List
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid
from .illness_photo import illness_photo
from .plant_family_illness import plant_family_illness
from .plant_variety_illness import plant_variety_illness


if TYPE_CHECKING:
    from .photo import Photo
    from .plant_family import PlantFamily
    from .plant_variety import PlantVariety


class Illness(db.Model, ModelMixin):
    __tablename__ = "illnesses"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Fields
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)

    reason: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="")
    symptoms: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="")
    treatment: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="")

    # Relationships
    photos: orm.Mapped[List["Photo"]] = orm.relationship(secondary=illness_photo)
    plant_families: orm.Mapped[List["PlantFamily"]] = orm.relationship(
        secondary=plant_family_illness, back_populates="illnesses"
    )
    plant_varieties: orm.Mapped[List["PlantVariety"]] = orm.relationship(
        secondary=plant_variety_illness, back_populates="illnesses"
    )

    def __repr__(self):
        return f"<Id: {self.id}, Illness: {self.name}>"

    def __str__(self):
        return f"{self.name}"
