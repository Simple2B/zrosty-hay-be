from typing import List, TYPE_CHECKING
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid
from .planting_steps import PlantingStep


if TYPE_CHECKING:
    from .plant_variety import PlantVariety


class PlantingProgram(db.Model, ModelMixin):
    __tablename__ = "planting_programs"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    plant_variety_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("plant_varieties.id"))

    # Fields
    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=generate_uuid, index=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)
    planting_time: orm.Mapped[int] = orm.mapped_column(default=0)
    harvest_time: orm.Mapped[int] = orm.mapped_column(default=0)

    # Relationships
    steps: orm.Mapped[List["PlantingStep"]] = orm.relationship(
        back_populates="planting_program",
        primaryjoin=sa.and_(id == PlantingStep.planting_program_id, PlantingStep.is_deleted.is_(False)),
        order_by=PlantingStep.day.asc(),
    )
    plant_variety: orm.Mapped["PlantVariety"] = orm.relationship(back_populates="programs")

    def __repr__(self):
        return f"<PlantingProgram: {self.id}>"
