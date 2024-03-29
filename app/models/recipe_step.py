from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm


from app.database import db
from .utils import ModelMixin, generate_uuid


if TYPE_CHECKING:
    from .recipe import Recipe
    from .photo import Photo


class RecipeStep(db.Model, ModelMixin):
    __tablename__ = "recipe_steps"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    recipe_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey("recipes.id"), nullable=False)
    photo_id: orm.Mapped[int | None] = orm.mapped_column(sa.Integer, sa.ForeignKey("photos.id"))

    # Fields
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)

    step_number: orm.Mapped[int] = orm.mapped_column()
    instruction: orm.Mapped[str] = orm.mapped_column(sa.Text, default="")

    # Relationships
    recipe: orm.Mapped["Recipe"] = orm.relationship(back_populates="steps")
    photo: orm.Mapped["Photo"] = orm.relationship()

    def __repr__(self):
        return f"<RecipeStep: {self.id}>"
