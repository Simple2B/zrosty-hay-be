from typing import List, TYPE_CHECKING
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


from app.database import db
from .utils import ModelMixin, generate_uuid
from .plant_family_illness import plant_family_illness
from .plant_family_pest import plant_family_pest

if TYPE_CHECKING:
    from .plant_variety import PlantVariety
    from .illness import Illness
    from .pest import Pest


class PlantFamily(db.Model, ModelMixin):
    __tablename__ = "plant_families"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Fields
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
    updated_at: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
    features: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="", nullable=True)

    # Relationships
    illnesses: orm.Mapped[List["Illness"]] = orm.relationship(
        secondary=plant_family_illness, back_populates="plant_families"
    )
    pests: orm.Mapped[List["Pest"]] = orm.relationship(secondary=plant_family_pest, back_populates="plant_families")
    plant_varieties: orm.Mapped[List["PlantVariety"]] = orm.relationship(back_populates="family")

    def __repr__(self):
        return f"<Id: {self.id}, PlantFamily: {self.name}>"
