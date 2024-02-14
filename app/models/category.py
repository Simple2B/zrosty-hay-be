from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


from app.database import db
from .utils import ModelMixin, generate_uuid


class Category(db.Model, ModelMixin):
    __tablename__ = "categories"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Fields
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)

    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)

    def __repr__(self):
        return f"<Id: {self.id}, Category: {self.name}>"
