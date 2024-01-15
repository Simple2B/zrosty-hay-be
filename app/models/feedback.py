from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin


class Feedback(db.Model, ModelMixin):
    __tablename__ = "feedbacks"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    user_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    plant_variety_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("plant_varieties.id"), nullable=False
    )

    # Fields
    text: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="", nullable=True)
    created_at: orm.Mapped[str] = orm.mapped_column(sa.DateTime, default=datetime, nullable=False)
    updated_at: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    def __repr__(self):
        return f"<Feedback: {self.id}>"
