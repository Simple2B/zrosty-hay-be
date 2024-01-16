from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid


class Photo(db.Model, ModelMixin):
    __tablename__ = "photos"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    url_path: orm.Mapped[str] = orm.mapped_column(sa.String(512), default="")
    original_name: orm.Mapped[str | None] = orm.mapped_column(sa.String(256), default="")
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)

    def __repr__(self):
        return f"<Photo: {self.id}>"
