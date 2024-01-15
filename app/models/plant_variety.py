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
    from .plant_family import PlantFamily
    from .planting_program import PlantingProgram


class PlantVariety(db.Model, ModelMixin):
    __tablename__ = "plant_varieties"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    plant_family_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey("plant_families.id"), nullable=False)

    # Fields
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    features: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="", nullable=True)
    general_info: orm.Mapped[str] = orm.mapped_column(sa.String(2048), default="", nullable=True)
    temperature_info: orm.Mapped[str] = orm.mapped_column(sa.String(2048), default="", nullable=True)
    watering_info: orm.Mapped[str] = orm.mapped_column(sa.String(2048), default="", nullable=True)
    planting_min_temperature: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)
    planting_max_temperature: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)
    is_moisture_loving: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True, nullable=True)
    is_sun_loving: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False, nullable=True)
    ground_ph: orm.Mapped[int] = orm.mapped_column(sa.String(64), nullable=True)
    ground_type: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=True)
    can_plant_indoors: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False, nullable=True)

    # Relationships
    illnesses: orm.Mapped[List["Illness"]] = orm.relationship(
        secondary=plant_variety_illness, back_populates="plant_varieties"
    )
    pests: orm.Mapped[List["Pest"]] = orm.relationship(secondary=plant_variety_pest, back_populates="plant_varieties")
    family: orm.Mapped[List["PlantFamily"]] = orm.relationship(back_populates="plant_varieties")
    photos: orm.Mapped[List["Photo"]] = orm.relationship(secondary=plant_variety_photo)
    planting_program: orm.Mapped["PlantingProgram"] = orm.relationship(
        "PlantingProgram", back_populates="plant_variety"
    )

    def __repr__(self):
        return f"<Id: {self.id}, PlantVariety: {self.name}>"
