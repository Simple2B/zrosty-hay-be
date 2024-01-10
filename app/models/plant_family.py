from typing import List, TYPE_CHECKING
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


from app.database import db
from .utils import ModelMixin, generate_uuid
from .plant_family_plant import plant_family_plant
from .plant_family_illness import plant_family_illness
from .plant_family_pest import plant_family_pest

if TYPE_CHECKING:
    from .plant_variety import PlantVariety
    from .illness import Illness
    from .pest import Pest
    from .condition import Condition


class PlantFamily(db.Model, ModelMixin):
    __tablename__ = "plant_families"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
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

    features: orm.Mapped[str] = orm.mapped_column(
        sa.String(1024), default="", nullable=True
    )
    condition: orm.Mapped["Condition"] = orm.relationship("Condition", uselist=False)

    illness: orm.Mapped[List["Illness"]] = orm.relationship(
        secondary=plant_family_illness, back_populates="plant_families"
    )
    pests: orm.Mapped[List["Pest"]] = orm.relationship(
        secondary=plant_family_pest, back_populates="plant_families"
    )
    plants: orm.Mapped[List["PlantVariety"]] = orm.relationship(
        secondary=plant_family_plant, back_populates="plant_families"
    )
