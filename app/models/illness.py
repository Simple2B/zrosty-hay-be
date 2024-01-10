from typing import TYPE_CHECKING, List


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
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )

    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    reason: orm.Mapped[str] = orm.mapped_column(
        sa.String(1024), default="", nullable=True
    )
    symptoms: orm.Mapped[str] = orm.mapped_column(
        sa.String(1024), default="", nullable=True
    )
    treatment: orm.Mapped[str] = orm.mapped_column(
        sa.String(1024), default="", nullable=True
    )

    photos: orm.Mapped[List["Photo"]] = orm.relationship(secondary=illness_photo)
    plant_families: orm.Mapped[List["PlantFamily"]] = orm.relationship(
        secondary=plant_family_illness, back_populates="illnesses"
    )
    plant_varieties: orm.Mapped[List["PlantVariety"]] = orm.relationship(
        secondary=plant_variety_illness, back_populates="illnesses"
    )
