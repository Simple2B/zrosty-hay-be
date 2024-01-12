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
    path: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="", nullable=True)

    def __repr__(self):
        return f"<Photo: {self.id}>"
