from typing import TYPE_CHECKING, List


import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid
from .pest_photo import pest_photo
from .plant_family_pest import plant_family_pest
from .plant_variety_pest import plant_variety_pest


if TYPE_CHECKING:
    from .photo import Photo
    from .plant_family import PlantFamily
    from .plant_variety import PlantVariety


class Pest(db.Model, ModelMixin):
    __tablename__ = "pests"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Fields
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    symptoms: orm.Mapped[str] = orm.mapped_column(
        sa.String(1024), default="", nullable=True
    )
    treatment: orm.Mapped[str] = orm.mapped_column(
        sa.String(1024), default="", nullable=True
    )

    # Relationships
    photos: orm.Mapped[List["Photo"]] = orm.relationship(secondary=pest_photo)
    plant_families: orm.Mapped[List["PlantFamily"]] = orm.relationship(
        secondary=plant_family_pest, back_populates="pests"
    )
    plant_varieties: orm.Mapped[List["PlantVariety"]] = orm.relationship(
        secondary=plant_variety_pest, back_populates="pests"
    )

    def __repr__(self):
        return f"<Id: {self.id}, Pest: {self.name}>"

    def __str__(self):
        return f"{self.name}"
