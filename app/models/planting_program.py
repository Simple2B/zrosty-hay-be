from typing import List, TYPE_CHECKING


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
    plant_variety_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("plant_varieties.id"), nullable=False
    )

    # Fields
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    planting_time: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=0, nullable=True)
    harvest_time: orm.Mapped[int] = orm.mapped_column(sa.Integer, default=0, nullable=True)

    # Relationships
    steps: orm.Mapped[List["PlantingStep"]] = orm.relationship(
        order_by="PlantingStep.step_number", back_populates="planting_program"
    )
    plant_variety: orm.Mapped["PlantVariety"] = orm.relationship("PlantVariety", back_populates="planting_program")

    def __repr__(self):
        return f"<PlantingProgram: {self.id}>"
