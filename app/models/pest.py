from typing import TYPE_CHECKING, List
from datetime import datetime

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
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)
    symptoms: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="")
    treatment: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="")

    # Relationships
    photos: orm.Mapped[List["Photo"]] = orm.relationship(secondary=pest_photo)
    plant_families: orm.Mapped[List["PlantFamily"]] = orm.relationship(
        secondary=plant_family_pest, back_populates="pests"
    )
    plant_varieties: orm.Mapped[List["PlantVariety"]] = orm.relationship(
        secondary=plant_variety_pest, back_populates="pests"
    )

    @property
    def json(self):
        from app.schema import Pest as PestSchema

        pest = PestSchema.model_validate(self)
        return pest.model_dump_json()

    def __repr__(self):
        return f"<Id: {self.id}, Pest: {self.name}>"

    def __str__(self):
        return f"{self.name}"
