import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin


class PlantingStep(db.Model, ModelMixin):
    __tablename__ = "planting_steps"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    planting_program_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("planting_programs.id"), nullable=False
    )

    day: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)
    step_number: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)
    instruction: orm.Mapped[str] = orm.mapped_column(
        sa.String(2046), default="", nullable=True
    )
