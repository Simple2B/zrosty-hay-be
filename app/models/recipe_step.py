from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm


from app.database import db
from .utils import ModelMixin, generate_uuid


if TYPE_CHECKING:
    from .recipe import Recipe


class RecipeStep(db.Model, ModelMixin):
    __tablename__ = "recipe_steps"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    recipe_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("recipes.id"), nullable=False
    )

    # Fields
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    step_number: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)
    instruction: orm.Mapped[str] = orm.mapped_column(
        sa.String(2046), default="", nullable=True
    )

    # Relationships
    recipe: orm.Mapped["Recipe"] = orm.relationship(back_populates="steps")

    def __repr__(self):
        return f"<RecipeStep: {self.id}>"
