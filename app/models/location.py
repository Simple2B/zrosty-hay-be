from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db

from .utils import ModelMixin


class Location(db.Model, ModelMixin):
    __tablename__ = "locations"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    country: orm.Mapped[str] = orm.mapped_column(sa.String(256), default="", index=True)
    region: orm.Mapped[str] = orm.mapped_column(sa.String(256), default="")
    city: orm.Mapped[str] = orm.mapped_column(sa.String(256), default="", index=True)

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )

    def __repr__(self):
        return f"<{self.country} {self.city}>"
