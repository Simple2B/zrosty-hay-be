import sqlalchemy as sa
from sqlalchemy import orm


from app.database import db
from .utils import ModelMixin, generate_uuid


class RecipeStep(db.Model, ModelMixin):
    __tablename__ = "recipe_steps"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    recipe_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("recipes.id"), nullable=False
    )

    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )

    step_number: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)
    instruction: orm.Mapped[str] = orm.mapped_column(
        sa.String(2046), default="", nullable=True
    )
