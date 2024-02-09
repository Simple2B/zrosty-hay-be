import enum
from typing import TYPE_CHECKING, List
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


from app.database import db
from .utils import ModelMixin, generate_uuid

from .plant_variety_illness import plant_variety_illness
from .plant_variety_pest import plant_variety_pest
from .plant_variety_category import plant_variety_category
from .plant_variety_photo import plant_variety_photo
from .photo import Photo

if TYPE_CHECKING:
    from .illness import Illness
    from .pest import Pest
    from .plant_category import PlantCategory
    from .plant_family import PlantFamily
    from .planting_program import PlantingProgram


class CareType(enum.Enum):
    easy = "easy"
    normal = "normal"
    hard = "hard"


class PlantVariety(db.Model, ModelMixin):
    __tablename__ = "plant_varieties"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    plant_family_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("plant_families.id"))

    # Fields
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        index=True,
        default=generate_uuid,
    )
    features: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="")
    general_info: orm.Mapped[str] = orm.mapped_column(sa.String(2048), default="")
    temperature_info: orm.Mapped[str] = orm.mapped_column(sa.String(2048), default="")
    watering_info: orm.Mapped[str] = orm.mapped_column(sa.String(2048), default="")
    min_temperature: orm.Mapped[float | None] = orm.mapped_column()
    max_temperature: orm.Mapped[float | None] = orm.mapped_column()

    min_size: orm.Mapped[float] = orm.mapped_column()
    max_size: orm.Mapped[float] = orm.mapped_column()
    humidity_percentage: orm.Mapped[float] = orm.mapped_column(default=0)
    water_volume: orm.Mapped[float] = orm.mapped_column(default=0)
    # must be enum
    care_type: orm.Mapped[str] = orm.mapped_column(sa.String(64), default=CareType.easy.value)

    is_moisture_loving: orm.Mapped[bool] = orm.mapped_column(default=True)
    is_sun_loving: orm.Mapped[bool] = orm.mapped_column(default=False)
    ground_ph: orm.Mapped[float | None] = orm.mapped_column()
    ground_type: orm.Mapped[str] = orm.mapped_column(sa.String(256), default="")
    can_plant_indoors: orm.Mapped[bool] = orm.mapped_column(default=False)

    # Relationships
    illnesses: orm.Mapped[List["Illness"]] = orm.relationship(
        secondary=plant_variety_illness, back_populates="plant_varieties"
    )
    pests: orm.Mapped[List["Pest"]] = orm.relationship(secondary=plant_variety_pest, back_populates="plant_varieties")
    family: orm.Mapped["PlantFamily"] = orm.relationship(back_populates="plant_varieties")
    photos: orm.Mapped[List["Photo"]] = orm.relationship(
        secondary=plant_variety_photo,
        viewonly=True,
        secondaryjoin=sa.and_(
            plant_variety_photo.c.plant_variety_id == id,
            plant_variety_photo.c.photo_id == Photo.id,
            Photo.is_deleted.is_(False),
        ),
    )
    _photos: orm.Mapped[List["Photo"]] = orm.relationship(
        secondary=plant_variety_photo,
    )
    programs: orm.Mapped[List["PlantingProgram"]] = orm.relationship(
        "PlantingProgram",
        back_populates="plant_variety",
    )
    categories: orm.Mapped[List["PlantCategory"]] = orm.relationship(secondary=plant_variety_category)

    @property
    def photo(self) -> str | None:  # type:ignore
        if self.photos:
            return self.photos[0]

    @property
    def watering(self) -> CareType:
        if self.water_volume < 500:
            return CareType.easy
        elif self.water_volume < 1000:
            return CareType.normal
        else:
            return CareType.hard

    def __repr__(self):
        return f"<Id: {self.id}, PlantVariety: {self.name}>"
