from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin


class PlantingStepType(db.Model, ModelMixin):
    __tablename__ = "planting_step_types"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    # Fields
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)

    def __repr__(self):
        return f"<StepType: {self.id}, name: {self.name}>"
