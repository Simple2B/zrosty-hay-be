from typing import List


import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid

from .planting_steps import PlantingStep


class PlantingProgram(db.Model, ModelMixin):
    __tablename__ = "planting_programs"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )

    planting_time: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, default=0, nullable=True
    )

    steps: orm.Mapped[List["PlantingStep"]] = orm.relationship(
        order_by="PlantingStep.step_number", back_populates="planting_program"
    )
