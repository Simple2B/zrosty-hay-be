from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid

if TYPE_CHECKING:
    from .planting_program import PlantingProgram
    from .planting_step_type import PlantingStepType


class PlantingStep(db.Model, ModelMixin):
    __tablename__ = "planting_steps"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        index=True,
        default=generate_uuid,
    )

    # Foreign keys
    planting_program_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("planting_programs.id"))
    step_type_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("planting_step_types.id"))

    # Fields
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)

    day: orm.Mapped[int] = orm.mapped_column(nullable=False)
    instruction: orm.Mapped[str] = orm.mapped_column(sa.Text, default="")

    # Relationships
    planting_program: orm.Mapped["PlantingProgram"] = orm.relationship(back_populates="steps")
    step_type: orm.Mapped["PlantingStepType"] = orm.relationship()

    @property
    def color(self):
        return self.step_type.color

    def __repr__(self):
        return f"<PlantingStep: {self.id}>"
