from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid
from .recipe_photo import recipe_photo
from .plant_family_recipe import plant_family_recipe
from .recipe_step import RecipeStep


if TYPE_CHECKING:
    from .plant_family import PlantFamily
    from .photo import Photo


class Recipe(db.Model, ModelMixin):
    __tablename__ = "recipes"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )

    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )

    cooking_time: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, default=0, nullable=True
    )

    plant_ingredients: orm.Mapped[List["PlantFamily"]] = orm.relationship(
        back_populates="recipes", secondary=plant_family_recipe
    )
    additional_ingredients: orm.Mapped[str] = orm.mapped_column(
        sa.String(1024), default="", nullable=True
    )
    photos: orm.Mapped[List["Photo"]] = orm.relationship(secondary=recipe_photo)
    steps: orm.Mapped[List["RecipeStep"]] = orm.relationship(
        order_by="RecipeStep.step_number", back_populates="recipe"
    )
